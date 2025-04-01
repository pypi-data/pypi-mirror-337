# Blog Link Extractor & Content Handler (BLECH)

BLECH is a tool designed to automatically identify and extract links to individual posts from a blog's main page, index, or feed. After identifying the links, it proceeds to fetch and parse the content of each blog post, making it easier to process, analyze, or archive blog data.

## Installation

### From PyPI (Recommended)

```bash
# Install using pip
pip install blech
```

### From Source

This project uses Poetry for dependency management. To install from source:

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository and install dependencies:
```bash
git clone https://github.com/jkarenko/blog-link-extractor-content-handler
cd blog-link-extractor-content-handler
poetry install
```

## Development

To run the development version:
```bash
poetry run blech [OPTIONS] <BASE_URL>
```

## Publishing to PyPI

To publish this package to PyPI:

1. Make sure you have the latest version of Poetry:
```bash
poetry self update
```

2. Build the package:
```bash
poetry build
```

3. Publish to PyPI (you'll need a PyPI account and API token):
```bash
# For the first time publishing
poetry publish --username __token__ --password your_api_token

# For subsequent updates
poetry publish --build
```

For more information on obtaining a PyPI API token, visit: https://pypi.org/help/#apitoken

## Usage

```bash
blech [OPTIONS] <BASE_URL>
```

### Positional Arguments:

*   `<BASE_URL>`: (Required) The starting URL of the blog's main page, index, or feed where post links can be found.

### Options:

*   `-o`, `--output <FILENAME>`: (Optional) The file where extracted content should be saved. If not provided, a default filename will be generated based on the blog's domain (e.g., `example-blog.com_blog_posts.txt`).
*   `-l`, `--lang <LANG_CODE>`: (Optional) Filter posts by language code (e.g., 'en', 'fi'). This primarily works when the blog uses a WordPress REST API that supports language filtering.
*   `--one-file`: (Optional) Save all blog posts to a single file instead of separate files. By default, each post is saved as a separate file in a directory named based on the output filename without the .txt extension (e.g., `example-blog.com_blog_posts`).
*   `--max-pages <NUMBER>`: (Optional) Maximum number of pages to fetch. Overrides the default limit (10 pages).
*   `--start-page <NUMBER>`: (Optional) Starting page number for scraping. Default is 1.
*   `--end-page <NUMBER>`: (Optional) Ending page number for scraping. Default is the value of max-pages.
*   `--posts-per-page <NUMBER>`: (Optional) Number of posts to fetch per API request. Overrides the default value (20 posts).
*   `-h`, `--help`: (Optional) Show this help message and exit.

### Example:

```bash
# Scrape English posts from the blog archive and save to a specific file
poetry run blech --output my_blog_extract.txt --lang en https://example-blog.com/archive

# Scrape all posts and use the default filename
poetry run blech https://another-blog.org/

# Scrape posts and save each one as a separate file in a directory (default behavior)
poetry run blech https://example-blog.com/

# Scrape posts, specify output directory name, and save as separate files
poetry run blech --output custom_dir_name.txt https://example-blog.com/

# Scrape posts and save all to a single file
poetry run blech --one-file https://example-blog.com/

# Scrape posts, specify output filename, and save to a single file
poetry run blech --output custom_file_name.txt --one-file https://example-blog.com/

# Scrape posts with pagination control (fetch up to 20 pages)
poetry run blech --max-pages 20 https://example-blog.com/

# Scrape posts starting from page 3
poetry run blech --start-page 3 https://example-blog.com/

# Scrape posts from page 2 to page 5 only
poetry run blech --start-page 2 --end-page 5 https://example-blog.com/

# Scrape posts with 50 posts per API request (instead of the default 20)
poetry run blech --posts-per-page 50 https://example-blog.com/
