# Runalytics

## Roadmap

- [ ] Read and extract data from .FIT garmin files to get power and efficiency data
- [ ] Identify the type of training automatically (by hand or by classifying and then running a machine learning algorithm? Use mechanical turk for classification)
        - Applying some rules based on JAck Daniels and Joe Friel on how much time you can stay at different levels, etc. could help
        - For some training sessions we can take those as reference points (e.g. races or runs with a title that describes the session, or weekly long runs)
- [ ] Identify races automatically (by hand or classifying and then running machine learning? Mechannical turk?)
- [ ] Identify runs with same route or parts of a route so they can be used for benchmarking and as if they were 'form tests'
- [ ] Divide form in 3-4 elements, build model that explains performance based on those elements to then understand how to benchmar the different elements and how training improves each component 


## Fixes

- [ ] Fix get_strava_key to look for Strava key instead of returning the first key in the list

- [ ] Add an empty activity to the analysis fixtures
- [ ] Add an activity with incorrect values (e.g. negative time) to the analysis features
- [ ] Add a long activity to the analysis fixtures

- [ ] Change trimp function to use right constant for male or female athlete

## Technical roadmap

- [ ] Update to Python 3.7
- [ ] Use a separate file to store paths to API endpoits and get calls from there
- [ ] Split pure helper methods from JustleticUser, etc. in separate files
- [ ] Modify STRAVA_ACTIVITIES fixture and activities tests to test that activities is ordered by date even if activities come unordered

## Other

Try to do a predictive model for 'speed' or 'pace' or 'power' based on:
    - Effort put in - 'hrm'
    - Fitness - 'TRIMP(CTL)'
    - Accumulated fatigue - 'TRIMP(ATL)'
    - In session fatigue - '???'
    - Temperature -
    - Hydration - ???
    - Running technique - ''
    - Elevation gradient
    - HRV data - ???
    
This model will be useful for:
    - Understanding the level of fitness and fatigue needed for a specific performance


## NOTES ##

Potential basic analysis workflow:
    1. Get data
    2. Featurize (e.g. run time series analysis to calculate fields for the model like number of segments, max and average of each segment, duration per segment, etc.)
    3. Buld rectangular dataset using original data and calculated features
    4. Run machine learning models

Think about whole infrastructure:
    Big question about making it synchronous vs asynchronous
   e.g. from https://www.youtube.com/watch?v=ZgHGCfwExw0 (min 17:00)
            - React + Redux frontend
            - Consumes data from a Django/Flask webserver
            - Celery workers dispatching analysis tasks


https://pandas.pydata.org/pandas-docs/stable/dsintro.html

http://scikit-learn.org
http://seaborn.pydata.org/tutorial.html
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4213373/
https://www.ncbi.nlm.nih.gov/pubmed/12840641
http://fellrnr.com/wiki/TRIMP
http://fellrnr.com/wiki/Heart_Rate_Reserve
http://fellrnr.com/wiki/Modeling_Human_Performance
http://fellrnr.com/wiki/Training_Monotony

https://towardsdatascience.com/mongodb-vs-pandas-5abe2c5ff6f3

