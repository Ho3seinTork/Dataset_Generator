import os
import json
import requests
import argparse
import markdown
import time
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from deepseek import Deepseek
import pandas as pd

class DatasetGenerator:
    def __init__(self, api_key, google_api_key, google_cse_id, output_markdown_path="output_dataset.md"):
        """
        Initialize the DatasetGenerator.
        
        Args:
            api_key (str): Deepseek API key
            google_api_key (str): Google API key for search
            google_cse_id (str): Google Custom Search Engine ID
            output_markdown_path (str): Path to output markdown file
        """
        self.deepseek = Deepseek(api_key=api_key)
        self.google_api_key = google_api_key
        self.google_cse_id = google_cse_id
        self.output_markdown_path = output_markdown_path
        
    def google_search(self, query, num_results=10):
        """
        Perform a Google search using Google Custom Search API.
        
        Args:
            query (str): Search query
            num_results (int): Number of search results to return
            
        Returns:
            list: List of search results (title, link, snippet)
        """
        try:
            service = build("customsearch", "v1", developerKey=self.google_api_key)
            result = service.cse().list(q=query, cx=self.google_cse_id, num=num_results).execute()
            
            search_results = []
            if "items" in result:
                for item in result["items"]:
                    search_results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", "")
                    })
            
            return search_results
        except Exception as e:
            print(f"Error during Google search: {str(e)}")
            return []
            
    def fetch_page_content(self, url):
        """
        Fetch and parse content from a webpage.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            str: Extracted text content from the webpage
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text
            text = soup.get_text(separator="\n")
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return ""
            
    def generate_dataset(self, topic, size, search_queries=None):
        """
        Generate a dataset based on the given topic and size.
        
        Args:
            topic (str): The main topic/domain for the dataset
            size (int): The number of entries to generate
            search_queries (list, optional): List of search queries to use instead of generating them
            
        Returns:
            list: The generated dataset
        """
        # Step 1: Generate search queries based on the topic if not provided
        if not search_queries:
            prompt = f"""
            I need to create a comprehensive dataset about "{topic}". 
            Please generate {min(10, size)} specific search queries that will help gather 
            diverse and high-quality information for this dataset.
            Each search query should focus on a different aspect or subtopic of "{topic}".
            Return only the search queries as a numbered list.
            """
            
            response = self.deepseek.generate(prompt=prompt, max_tokens=1000)
            search_queries = self._extract_queries_from_response(response)
        
        # Step 2: Perform Google searches for each query
        search_results = []
        for query in search_queries[:min(10, size)]:
            results = self.google_search(query, num_results=5)
            search_results.extend(results)
            time.sleep(1)  # Sleep to avoid hitting API rate limits
        
        # Step 3: Fetch and extract content from the search results
        source_materials = []
        for result in search_results[:size * 2]:  # Get twice as many sources as needed entries
            content = self.fetch_page_content(result["link"])
            if content:
                source_materials.append({
                    "title": result["title"],
                    "content": content[:5000],  # Limit content length
                    "url": result["link"]
                })
            time.sleep(1)  # Sleep to avoid overloading servers
        
        # Step 4: Generate dataset entries using Deepseek
        dataset = []
        
        batch_size = min(5, size)  # Process in batches to avoid token limits
        for i in range(0, size, batch_size):
            current_batch_size = min(batch_size, size - i)
            
            # Select relevant source materials for this batch
            batch_sources = source_materials[i:i+current_batch_size*2]
            sources_text = "\n\n".join([
                f"Source {j+1}: {source['title']}\n{source['content'][:1000]}"
                for j, source in enumerate(batch_sources)
            ])
            
            prompt = f"""
            Based on the following sources about "{topic}", create {current_batch_size} high-quality dataset entries.
            
            {sources_text}
            
            For each entry, include:
            1. A title or identifier
            2. A comprehensive description
            3. Key attributes or properties (at least 5)
            4. Relations to other concepts in the domain
            5. Citation information
            
            Format each entry as a JSON object with the following structure:
            {{
                "id": "unique identifier",
                "title": "entry title",
                "description": "comprehensive description",
                "attributes": {{"attribute1": "value1", "attribute2": "value2", ...}},
                "relations": [{{"relation_type": "type", "related_to": "entity"}}],
                "source": "citation information"
            }}
            
            Return the entries as a valid JSON array.
            """
            
            response = self.deepseek.generate(prompt=prompt, max_tokens=4000)
            batch_entries = self._extract_json_from_response(response)
            
            if batch_entries:
                dataset.extend(batch_entries)
            
            time.sleep(2)  # Sleep to avoid API rate limits
        
        # Ensure we have the correct number of entries
        dataset = dataset[:size]
        
        # Save to markdown file
        self._save_to_markdown(dataset, topic)
        
        return dataset
    
    def _extract_queries_from_response(self, response):
        """Extract search queries from the model response"""
        lines = response.strip().split("\n")
        queries = []
        
        for line in lines:
            # Match numbered or bulleted list items
            if line.strip() and (line.strip()[0].isdigit() or line.strip()[0] in ["•", "-", "*"]):
                # Remove number/bullet and clean
                query = line.strip()
                for prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "•", "-", "*"]:
                    if query.startswith(prefix):
                        query = query[len(prefix):].strip()
                        break
                
                if query:
                    queries.append(query)
        
        # If no formatted list was found, just split by newlines and take non-empty lines
        if not queries:
            queries = [line.strip() for line in lines if line.strip()]
            
        return queries
    
    def _extract_json_from_response(self, response):
        """Extract JSON data from the model response"""
        try:
            # Find the start and end of the JSON array
            start_idx = response.find("[")
            end_idx = response.rfind("]") + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            
            # If not found as an array, try to find individual JSON objects
            entries = []
            potential_jsons = response.split("}\n{")
            
            for i, json_part in enumerate(potential_jsons):
                if i == 0:
                    json_part = json_part + "}"
                elif i == len(potential_jsons) - 1:
                    json_part = "{" + json_part
                else:
                    json_part = "{" + json_part + "}"
                
                try:
                    entry = json.loads(json_part)
                    entries.append(entry)
                except:
                    continue
            
            return entries
        except Exception as e:
            print(f"Error extracting JSON from response: {str(e)}")
            return []
    
    def _save_to_markdown(self, dataset, topic):
        """Save the dataset to a markdown file"""
        with open(self.output_markdown_path, "w", encoding="utf-8") as f:
            f.write(f"# Dataset: {topic}\n\n")
            f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Number of entries: {len(dataset)}\n\n")
            
            for i, entry in enumerate(dataset):
                f.write(f"## Entry {i+1}: {entry.get('title', 'Untitled')}\n\n")
                
                f.write(f"### Description\n\n")
                f.write(f"{entry.get('description', 'No description')}\n\n")
                
                f.write(f"### Attributes\n\n")
                if "attributes" in entry and entry["attributes"]:
                    for key, value in entry["attributes"].items():
                        f.write(f"- **{key}**: {value}\n")
                else:
                    f.write("No attributes specified\n")
                f.write("\n")
                
                f.write(f"### Relations\n\n")
                if "relations" in entry and entry["relations"]:
                    for relation in entry["relations"]:
                        f.write(f"- **{relation.get('relation_type', 'Related to')}**: {relation.get('related_to', 'Unknown')}\n")
                else:
                    f.write("No relations specified\n")
                f.write("\n")
                
                f.write(f"### Source\n\n")
                f.write(f"{entry.get('source', 'No source information')}\n\n")
                
                f.write("---\n\n")
            
            print(f"Dataset saved to {self.output_markdown_path}")

    def export_to_csv(self, dataset, output_path="dataset.csv"):
        """Export the dataset to a CSV file"""
        flattened_data = []
        
        for entry in dataset:
            flat_entry = {
                "id": entry.get("id", ""),
                "title": entry.get("title", ""),
                "description": entry.get("description", "")
            }
            
            # Flatten attributes
            if "attributes" in entry and entry["attributes"]:
                for key, value in entry["attributes"].items():
                    flat_entry[f"attribute_{key}"] = value
            
            # Add source
            flat_entry["source"] = entry.get("source", "")
            
            flattened_data.append(flat_entry)
        
        df = pd.DataFrame(flattened_data)
        df.to_csv(output_path, index=False)
        print(f"Dataset exported to CSV: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate a dataset with Deepseek LLM and Google Search")
    parser.add_argument("--topic", required=True, help="The main topic for the dataset")
    parser.add_argument("--size", type=int, default=10, help="Number of entries to generate")
    parser.add_argument("--output", default="output_dataset.md", help="Output markdown file path")
    parser.add_argument("--csv", default="dataset.csv", help="Output CSV file path")
    parser.add_argument("--deepseek_api_key", required=True, help="Deepseek API key")
    parser.add_argument("--google_api_key", required=True, help="Google API key")
    parser.add_argument("--google_cse_id", required=True, help="Google Custom Search Engine ID")
    
    args = parser.parse_args()
    
    generator = DatasetGenerator(
        api_key=args.deepseek_api_key,
        google_api_key=args.google_api_key,
        google_cse_id=args.google_cse_id,
        output_markdown_path=args.output
    )
    
    dataset = generator.generate_dataset(args.topic, args.size)
    generator.export_to_csv(dataset, args.csv)
    
    print(f"Generated {len(dataset)} entries about '{args.topic}'")
    print(f"Results saved to {args.output} and {args.csv}")


if __name__ == "__main__":
    main()
