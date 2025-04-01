
# cleancourt

[![PyPi page link -- version](https://img.shields.io/pypi/v/cleancourt.svg)](https://pypi.python.org/pypi/cleancourt)
[![Current Issues](https://img.shields.io/bitbucket/issues/lsc_odga/cleancourt.svg)](https://bitbucket.org/lsc_odga/cleancourt/issues)


cleancourt cleans, standardizes, and links legal party names using  natural language processing and string similarity search algorithms. At this time, CC is primarily tested and used on company names. These processes are thus effective for cleaning and standardizing parties to understand top filers in eviction cases, for example, as these top filers are typically company names. These processes are much more exploratory when it comes to individuals. That is, cleaning and standardizing individual names is still in the exploratory stages. 

While this dataset has only been tested on party information in civil court cases, the methods may work in other contexts. These applications, however, are untested and, as such, we can make no assertions that the validity of their output.

**Note:** This library employs AI methods to clean and standardize party names. If you are unfamiliar with deploying and testing AI models, please reach out to the author for assistance.

## Set up

```bash
pip install --upgrade cleancourt
```

## Functionality
The cleancourt library has two central functionalities. The first is internal dataset cleaning, which takes in a list of party names and returns a sanitized list that makes a best guess effort at fuzzy matching party names. The second cleancourt functionality is party name comparison to an external dataset. This functionality, which employs similar methods to internal dataset cleaning, is used when comparing a list of 'messy' party names against a list of 'clean' party names.

### Main Functions

#### full_clean_names

```python
cleancourt.full_clean_names(
  messy_name_list,
  separate_management=False,
  min_similarity_score=.80,
  party_type = 'None Specified'

)
```
The full_clean_names function takes in a list of messy names in the dataset and applies all name cleaning functions to said dataset. The function first cleans the data using pattern matching, then separates the data based on whether a party name refers to an individual or a company. From there, the two datasets are cleaned in isolation using the format_people_names or the link_company_names discussed below. The datasets are then rejoined and linked one more time by removing spaces using the check_spaces function.

The full_clean_names function also takes in an optional boolean parameter to determine whether or not a party name should be separated into two separate lists when a management company is present. When set to True, the party name 'A doing business as B', for example, would be separated into two lists, where B is put in the original column, and A is added to a _managing companies_ column. When set to True, the function will return two lists.

Another optional parameter taken by full_clean_names is the min_similarity_score parameter, which is passed directly to the link_company_names function and used to compute the threshold for similarity among company names.

As of CC 0.8.0, full_clean_names now takes an optional party_type parameter. You can use this parameter should you wish to skip the labeling of entities as either people or companies. In order to skip this ordering, you must supply a value of either 'person' or 'company' depending on the list type that you are supplying.

#### compare_companies

```python
cleancourt.compare_companies(
	org_name_messy,
	org_name_clean,
	threshold=.25,
	print_all_matches = False,
	clean_org_names = [False, False]
	)
```

The compare_companies function takes in a _messy_ list of party names and a _clean_ list of company names and filters out the individual names in the messy dataset before comparing both names.

The function takes in a list of optional parameters. _threshold_ is the maximum distance between two names being compared that will be included in the name matching. _print\_all\_matches_ is an internal print function to test functionality, matches returned are printed to a local CSV file. clean_org_names is a boolean array that takes in two values. When set to true, the function will apply the clean_data function to the corresponding list or party names.


### Internal Dataset Cleaning

For cleaning datasets in isolation, cleancourt currently has four functions, each of which are detailed below. All functions, with the exception of clean_data, take in a list of party names, and return a dictionary with the original names as keys, and the mapped names as values.

#### clean_data
clean_data is the preprocessing function used to ensure that the data is in readable form, and that any minor changes to each string can be made. The method primarily employs regular expression formulas to format and edit the data. This preprocessing step is specifically geared towards cleaning civil court case party names. As such, you may wish to overwrite this function in favor of a data cleaning step that is more applicable to your data.

#### format_people_names
The format_people_names function uses the probablepeople library to find individual names (rather than corporate entities) in the dataset, and parse their first, middle, and last names. The function takes a Pandas DataFrame of names and outputs a dictionary of names in first, middle, last format. As an example, consider the following dataset:

|raw_name|
|--------|
|aldous huxley|
|huxley, aldous|
|ray bradbury|
|bradbury, ray|

The format_people_names function would then return the following dictionary:

```json
{
"aldous huxley": "aldous huxley",
"huxley, aldous" : "aldous huxley",
"ray bradbury": "ray bradbury",
"bradbury, ray": "ray bradbury"
}
```

#### link_company_names

The link_company_names function takes in a Pandas DataFrame, along with an optional score threshold, and returns a dictionary of key-value pairs in which the key is a particular entry in the DataFrame and the associated value is the linked company determined to by similar to the key by a fuzzy match algorithm. To compute this similarity between strings at scale, we first begin by filtering company names from the dataset using the probablepeople library.

Once a set of unique company names has been developed, the algorithms used to determine similarity between strings is dependent upon the number of company names being compared. If fewer than 500 company names exist, then we compute the Levenshtein distance. Otherwise we compute scores using Term Frequency Inverse Document Frequency (TF-IDF) and cosine similarities. These methods are used because Levenshtein distance is simple, but time intensive on larger datasets, while TF-IDF and cosine simmilarities scale well for larger datasets, but underperform on smaller datasets.  Both of these methods are discussed below.

##### Levenshtein Distance

This function employs the [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) library to compute a similarity score between a particular name, and all other names in the dataset. By default, all names with a similarity score above 80% are considered the same and linked using a dictionary format. See below for a more detailed discussion of the link_company_names output.


##### TFIDF and Cosine similarities

For datasets larger than 500 names, when a particular string is determined to be a company name, we vectorize it using TF-IDF. Using an ngram of three characters, we first separate the company name into an array of chunks such that the company name 'wayne enterprises' will produce the following array:

```python
['way', 'ayn', 'yne', 'ne ', 'e e', ' en', 'ent', 'nte', 'ter', 'erp', 'rpr', 'pri', 'ris', 'ise', 'ses']
```


Once these arrays have been created for every company name in the dataset, we then create a sparse matrix, which contains all ngrams computed for all company names as one dimension, and all company names as the other dimension. The value at each index within this matrix is then the term frequency of an ngram chunk in a particular company name, multiplied by the inverse frequency of that ngram chunk across all company names. Thus, ngrams that appear frequently across all documents will bring the value at a particular index closer to 0.

In this case, ngrams of three characters were chosen as they are particularly effective at creating a sparse matrix of sufficient size, while also containing enough characters to make each individual ngram unique.

Once we have calculated the scores for each ngram chunk across each document, we then compute the cosine similarity between each document. The cosine similarity is computed by summing the products of each document vector, and dividing it by the square root of the sum of squares of each document vector, multiplied together. To illustrate how this works, consider the following two documents and their vectors computed using TF-IDF.

```python
doc1 = [0,2,1,3,5]
doc2 = [4,2,3,4,1]
```

The cosine similarity of these two documents would be:

```python
doc1 * doc2 = 0*4 + 2*2 + 1*3 + 3*4 + 5*1 = 24
||doc1|| = sqrt(0^2 + 2^2 + 1^2 + 3^2 + 5^2) = 6.1644...
||doc2|| = sqrt(4^2 + 2^2 + 3^2 + 4^2 + 1^2) = 6.7823...

cos_sim = 24 / (6.1644 * 6.7823) = .574

```

The resulting similarity score of these two documents is .574. Documents that are more similar will have a score closer to 1, while documents that are not similar will have a similarity score closer 0. Currently, this method considers all company names with a similarity score above .8 to be the same.


##### Output

Once the similarity scores have been computed, we take the resulting matches and place them in a dictionary where the key is the original company name, and the value is the company name that appears most frequently in the dataset. The following dataset, for example:

raw_name|raw_name_count
--------|--------------
wayne enterprise|10
wayne enterprises|2
wayn enterprises|4
lexcorp | 10
lexco | 5
lex corp. | 4

Would output the following dictionary:

```json
{
"wayne enterprises" : "wayne enterprise",
"wayn enterprises" : "wayne enterprise",
"lexco" : "lexcorp",
"lex corp." : "lexcorp"
}

```

#### check_spaces

The check_spaces is currently applied as a final step in the name standardization process. That is, check_spaces is intended to be run once all other methods have been completed.

The function takes in a Pandas DataFrame and returns a dictionary of key-value pairs in which the key is a particular entry in the DataFrame and the associated value is a linked name found to contain the exact same characters, except for spaces.

As with other functions in this library, the method for determining which value should be linked in the dataset is to select the value that appears the most in the dataset.

As an example consider the following dataset, which has grouped the original dataset by the raw name, counted the number of occurrences in the dataset, and also computed the equivalent name with no spaces:

raw_name | raw_name_count | no_space_name
-------- | -------------- | -------------
mary shelley | 10 | maryshelley
mary she lley | 1 | maryshelley
ma ryshelley | 1 | maryshelley
george orwell | 15 | georgeorwell
georg e orwell | 1 | georgeorwell
geor georwell | 3 | georgeorwell
g eorge orwell | 8 | georgeorwell


This dataframe will return the following dictionary:

```json
{
"mary shelley": "mary shelley",
"mary she lley" : "mary shelley",
"ma ryshelley" : "mary shelley",
"george orwell": "george orwell",
"georg e orwell" : "george orwell",
"geor georwell" : "george orwell",
"g eorge orwell" : "george orwell"
}
```

Rather than return the relevant string with no spaces as the value, the function takes the string with the highest raw_name_count and returns the associated raw_name. This functionality is based on the assumption that the term that appears most frequently in the original dataset is the correct version.


### Dataset Comparisons

The data output from CleanCourt are regular tested for accuracy by LSC's team of data engineers. In one such example, we assessed 4,500 names randomly pulled from court cases in Virginia. By manually assessing the validity of these names, we found that the CleanCourt model has a roughly 1% error rate, with a margin of error of ± 0.313%.

Because of the sensitivity of the data we are unable to make public any for testing purposes. However, if you would like more information regarding the accuracy of CleanCourt please reach out to the author.

## Authors

Logan Pratico: praticol{at}lsc{dot}gov

## Acknowledgments and References

### ML Python Libraries:
* [probablepeople](https://github.com/datamade/probablepeople)
* [sklearn](https://scikit-learn.org/stable/)
* [SciPy](https://scipy.org/)
* [rapidfuzz](https://github.com/maxbachmann/RapidFuzz)

### Resources and Articles Used to Inform this Library
* [TF-IDF from scratch in python on a real-world dataset](https://towardsdatascience.com/tf-idf-for-document-ranking-from-scratch-in-python-on-real-world-dataset-796d339a4089) - William Scott
* [Fuzzy Matching at Scale](https://towardsdatascience.com/fuzzy-matching-at-scale-84f2bfd0c536) -- Josh Taylor
* [Cosine Similarity // Data Mining: Concepts and Techniques](https://www.sciencedirect.com/topics/computer-science/cosine-similarity) -- Jiawei Han, Micheline Kamber and Jian Pei
* [The Optimization of Fuzzy String Matching Using TF-IDF and KNN](https://audhiaprilliant.medium.com/fuzzy-string-matching-optimization-using-tf-idf-and-knn-b07fce69b58f) -- Audhi Aprilliant
* [Text Classification using K Nearest Neighbors](https://towardsdatascience.com/text-classification-using-k-nearest-neighbors-46fa8a77acc5) -- Sumit Dua
