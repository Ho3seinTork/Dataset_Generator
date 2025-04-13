# Dataset Generator with Deepseek LLM and Google Search

[English](#english) | [فارسی](#persian)

<a name="english"></a>
## English

A Python tool that generates high-quality datasets using the Deepseek language model and Google search. This tool connects to a Markdown file and creates structured datasets based on your specified topic and size.

### Features

- **AI-Powered Topic Analysis**: Uses Deepseek LLM to analyze topics and generate appropriate search queries
- **Deep Web Search**: Leverages Google's API to find high-quality, verified sources
- **Intelligent Content Extraction**: Automatically extracts relevant information from web pages
- **Structured Data Generation**: Creates well-organized dataset entries with rich metadata
- **Dual Export Formats**: Saves datasets in both Markdown and CSV formats for versatile usage

### Requirements

- Python 3.7+
- Deepseek API key
- Google API key
- Google Custom Search Engine ID

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dataset-generator.git
cd dataset-generator

# Install requirements
pip install -r requirements.txt
```

### Usage

```bash
python dataset_generator.py --topic "Your Topic" --size 20 --deepseek_api_key "YOUR_DEEPSEEK_API_KEY" --google_api_key "YOUR_GOOGLE_API_KEY" --google_cse_id "YOUR_GOOGLE_CSE_ID"
```

#### Parameters

- `--topic`: Main topic for the dataset (required)
- `--size`: Number of entries to generate (default: 10)
- `--output`: Output markdown file path (default: "output_dataset.md")
- `--csv`: Output CSV file path (default: "dataset.csv")
- `--deepseek_api_key`: Your Deepseek API key (required)
- `--google_api_key`: Your Google API key (required)
- `--google_cse_id`: Your Google Custom Search Engine ID (required)

### Output

The script generates two files in your working directory (or specified paths):

1. A Markdown file with rich formatting and comprehensive dataset information
2. A CSV file for easy import into data analysis tools and databases

### Example

```bash
python dataset_generator.py --topic "Quantum Computing" --size 15 --deepseek_api_key "your_key" --google_api_key "your_key" --google_cse_id "your_id"
```

This will generate a 15-entry dataset about Quantum Computing with detailed descriptions, attributes, relationships, and source citations.

### License

MIT

---

<a name="persian"></a>
## فارسی

یک ابزار پایتونی که با استفاده از مدل زبانی Deepseek و جستجوی گوگل، مجموعه داده‌های با کیفیت بالا تولید می‌کند. این ابزار به یک فایل مارکداون متصل می‌شود و بر اساس موضوع و اندازه مشخص شده، مجموعه داده‌های ساختاریافته ایجاد می‌کند.

### ویژگی‌ها

- **تحلیل موضوعی مبتنی بر هوش مصنوعی**: از مدل زبانی Deepseek برای تحلیل موضوعات و تولید پرس‌وجوهای جستجوی مناسب استفاده می‌کند
- **جستجوی عمیق وب**: از API گوگل برای یافتن منابع با کیفیت بالا و تأیید شده استفاده می‌کند
- **استخراج هوشمند محتوا**: به صورت خودکار اطلاعات مرتبط را از صفحات وب استخراج می‌کند
- **تولید داده‌های ساختاریافته**: ورودی‌های مجموعه داده با فراداده‌های غنی و سازمان‌یافته ایجاد می‌کند
- **فرمت‌های خروجی دوگانه**: مجموعه داده‌ها را در هر دو فرمت Markdown و CSV برای استفاده متنوع ذخیره می‌کند

### نیازمندی‌ها

- پایتون 3.7+
- کلید API مدل Deepseek
- کلید API گوگل
- شناسه موتور جستجوی سفارشی گوگل (CSE ID)

### نصب

```bash
# کلون کردن مخزن
git clone https://github.com/yourusername/dataset-generator.git
cd dataset-generator

# نصب وابستگی‌ها
pip install -r requirements.txt
```

### نحوه استفاده

```bash
python dataset_generator.py --topic "موضوع شما" --size 20 --deepseek_api_key "کلید_API_شما" --google_api_key "کلید_API_گوگل_شما" --google_cse_id "شناسه_CSE_شما"
```

#### پارامترها

- `--topic`: موضوع اصلی برای مجموعه داده (الزامی)
- `--size`: تعداد ورودی‌هایی که باید تولید شود (پیش‌فرض: 10)
- `--output`: مسیر فایل مارکداون خروجی (پیش‌فرض: "output_dataset.md")
- `--csv`: مسیر فایل CSV خروجی (پیش‌فرض: "dataset.csv")
- `--deepseek_api_key`: کلید API مدل Deepseek شما (الزامی)
- `--google_api_key`: کلید API گوگل شما (الزامی)
- `--google_cse_id`: شناسه موتور جستجوی سفارشی گوگل شما (الزامی)

### خروجی

اسکریپت دو فایل در دایرکتوری کاری شما (یا مسیرهای مشخص شده) تولید می‌کند:

1. یک فایل مارکداون با قالب‌بندی غنی و اطلاعات جامع مجموعه داده
2. یک فایل CSV برای ورود آسان به ابزارهای تحلیل داده و پایگاه‌های داده

### مثال

```bash
python dataset_generator.py --topic "محاسبات کوانتومی" --size 15 --deepseek_api_key "کلید_شما" --google_api_key "کلید_شما" --google_cse_id "شناسه_شما"
```

این دستور یک مجموعه داده 15 ورودی درباره محاسبات کوانتومی با توضیحات دقیق، ویژگی‌ها، روابط و استنادات منبع تولید می‌کند.

### مجوز

MIT
