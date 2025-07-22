# Contesting Islamophobia Tweet Analysis Tool
This repository contains some of the code developed as part of the AHRC funded project “<a href="https://www.keele.ac.uk/research/ourresearch/humanities/mediacultureandcreativepractice/contestingislamophobia/">#ContestingIslamophobia: Representation and Appropriation in Mediated Activism</a>" which examined the dynamics of anti- and pro-Muslim online activism. Using Twitter # campaigns as its starting point we focus on the appropriation of global ‘trigger’ events, such as terror attacks, by right wing US activists to create anti-Muslim narratives, and how these narratives are in turn opposed by anti-racist groups.

This repository does not contain the code developed to collect and filter tweets, only the code used to analyse tweets and create a number of files (csv, xlsx) and visualisations. 

## Getting Started
The code has been developed as a Jupyter Notebook and recently (22/7/25) tested on a JupyterHub. Due to the licensing agreements with twitter at the time, we are unable to share our full datasets and so have created an anonymised <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/blob/main/tweets/filtered/event/sub_event/data/example.json">example.json</a> file (in <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/tree/main/tweets/filtered/event/sub_event/data">analysis/tweets/filtered/event/sub_event/data</a>) that shows the format of our filtered and processed tweets (that we obtained from the v1.1 and v2.0 twitter API's). The event/sub_event structure related to the fact we had a number of trigger events that we analysed, split into discrete time segments. The <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/tree/main/analysis_config/event">analysis_config folder</a> contained config files for all of our events and sub_events; we have recreated an example version (<a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/blob/main/analysis_config/event/example.json">example.json</a>) to give an idea of some of the parameters and search terms we used. <code>"from_dir"</code> points to where the json files containing tweets were stored, and <code>"to_dir"</code> points to were the outputs from the analysis were saved to.

In order to get this running, you will need to place the 4 folders in your JupyterHub or equivalent at the top of the directory structure (or be prepared to edit the code to point to where the various files are stored).

<img width="2415" height="667" alt="JupyterHub Screenshot" src="https://github.com/user-attachments/assets/4a69b4e7-53f5-46d8-afb0-b96da03a3892" />

The <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/blob/main/analysis/twitter-analysis.ipynb">twitter-analysis.ipynb</a> notebook (in the <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/blob/main/analysis/">analysis folder</a>) does most of the analysis. You will need to comment in/out various <code>pip install</code> commands, dependent on your environment.

Once run, the code will create and output a number of different files that relate to the kinds of analysis that we were interested in.

<img width="1931" height="1576" alt="JupyterHub Screenshot" src="https://github.com/user-attachments/assets/89a19fca-ff17-4dad-9a81-65b0b9045fd4" />

At the moment, these are just using the 10 example tweets in the example.json file. If you did want to use this code to analyse your own dataset, you would need to convert it into this format (which is similar to the format the twitter API used to use).

You can read more about this in the <a href="https://github.com/eddequincey/contestingIslamophobia-tweet-analysis/blob/main/DOCUMENTATION.md">DOCUMENTATION.md</a>

## Acknowledgements
We would like to thank Matt Burke for gathering the data and initial programming and Ben Jolley for his fantastic programming skills and generating the datasets. This repository is mostly a combination of their work.

