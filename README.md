# Gender-bias-in-Wikipedia
Analyze Gender Bias in Wikipedia Articles

## Getting Started  

1. Download latest all titles dump from [here](https://dumps.wikimedia.org/enwiki/latest/) or follow [this link to download](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles.gz)  
2. Extract and move the `enwiki-latest-all-titles.txt` file to `/data` directory  
3. Install all the dependencies from the `requirements.txt` file as
`pip install -r requirements.txt`  
or   
Create conda environment as
`conda env create -f environment.yml`  

4. Run utils/extract_data.py to get users and gender info as
`python utils/extract_data.py`  