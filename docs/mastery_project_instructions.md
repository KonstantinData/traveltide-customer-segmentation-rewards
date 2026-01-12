Welcome to the Mastery Project!
This is your opportunity to apply everything you’ve learned in a real-world data challenge. The Mastery project is designed to simulate the type of data-driven decision-making you would be responsible for in a professional environment. You’ll work through data exploration, feature engineering, customer segmentation, and strategic recommendations, all while reinforcing your analytical and problem-solving skills.
This project is structured to mirror industry workflows, where you will go from understanding the problem to presenting a well-structured, data-backed strategy.
 
________________________________________
How This Course Prepares You
This mastery project is hands-on and results-driven, requiring you to think critically about data, draw meaningful insights, and present actionable recommendations. You’ll follow a structured process, working through different phases that gradually build toward a final business strategy.
Each stage is designed to develop your ability to work with raw data, transform it into valuable insights, and communicate your findings effectively—essential skills for any data professional.
________________________________________
 
Course Structure Overview
Week 1: Project Exploration
	Familiarize yourself with the dataset and business context.
	Understand key objectives and expectations for the final strategy.
Week 2: Feature Engineering & Customer Segmentation
	Execute Feature Engineering to improve data quality.
	Create meaningful data metrics to analyze user behavior.
Week 3: Developing Insights & Strategy
	Segment customers into distinct groups based on data patterns.
	Refine your data-driven recommendations based on customer insights.
Week 4: Presenting Your Findings
	Structure your final project submission with clear insights and justifications.
	Deliver a data-backed strategy in a professional format.
________________________________________
What This Course Offers
	Real-World Data Problem: Work with a business dataset and develop a complete analytical solution.
	End-to-End Project Experience: Move through every stage of a data project, from exploration to strategic recommendations.
	Portfolio-Ready Work: Develop a structured project that showcases your analytical and storytelling skills.
At the end of this course, you will:
	Uncover trends and insights in the data.
	Identify meaningful customer segments and develop business strategy.
	Present well-structured, data-driven recommendations.
________________________________________
 
Closing Thoughts
This mastery project is a culmination of your learning journey, providing the experience of tackling a real-world business problem. It challenges you to think critically, communicate effectively, and apply your skills in a structured way—just as you would in a professional setting.
Approach this project as a chance to refine your analytical thinking, strengthen your portfolio, and build confidence in working with data at scale.
Let’s dive in—your final challenge starts now! 🚀
 
 
Segmentation as an Analytical Task
In this project, you will segment customer data according to business needs and deliver data-driven recommendations based on your findings.
The project features four stages, each done in a week:
	Exploratory Data Analysis
	Feature Engineering
	Segmentation
	Presenting Results 
You will find the description of these steps and their goals at the end of this page, but first let’s explore what segmentation is and how it can help the stakeholders of a company that we are going to work with - the TravelTide company that we’ll introduce in details in the next lesson!
Let’s Deep Dive into Customer Segmentation
________________________________________
 
👆 What is segmentation?
You’ve already learned about segmentation while going through some of the courses in the program. Let’s briefly recap that segmentation refers to a broad category of analytic techniques that allow us to group similar data points.
⚠️ In this project, data points will represent customers, whom we will group according to their shopping behavior in the context of a very specific business initiative.
 
 
 
Segmentation as an Analytical Task
While this project focuses on segmenting customers based on their behavior, we want to emphasize that segmentation is a very general approach in data analysis that can be broadly applicable to just about every domain. Whenever we suspect a dataset has some natural but hidden structure, we can use segmentation to reveal it.
To illustrate this, let’s consider an example from cancer diagnostics.
 
Suppose we have an extensive collection of medical scans that physicians have not reviewed for abnormalities. Segmentation can be used to cluster scans with similar pixel patterns prior to the review by doctors. Then, instead of manually reviewing every scan, doctors can sample scans from each cluster to verify if any clusters correspond to abnormal images! This improves diagnostic speed, resulting in better patient care.

Let’s Deep Dive into Customer Segmentation
What is segmentation?
You’ve already learned about segmentation while going through some of the courses in the program. Let’s briefly recap that segmentation refers to a broad category of analytic techniques that allow us to group similar data points.
In this project, data points will represent customers, whom we will group according to their shopping behavior in the context of a very specific business initiative.  

Segmentation as an Analytical Task
While this project focuses on segmenting customers based on their behavior, we want to emphasize that segmentation is a very general approach in data analysis that can be broadly applicable to just about every domain. Whenever we suspect a dataset has some natural but hidden structure, we can use segmentation to reveal it.
To illustrate this, let’s consider an example from cancer diagnostics.
 
Suppose we have an extensive collection of medical scans that physicians have not reviewed for abnormalities. Segmentation can be used to cluster scans with similar pixel patterns prior to the review by doctors. Then, instead of manually reviewing every scan, doctors can sample scans from each cluster to verify if any clusters correspond to abnormal images! This improves diagnostic speed, resulting in better patient care.
Think about a domain you are particularly interested in - can you imagine a potential application of segmentation analysis in this domain?Possible applications
	Media: In journalism, segmentation can automatically categorize news stories into different topics for efficient news management and distribution.
	Sports: Sports analysts can use segmentation to group players based on ability. This can help team managers make informed decisions about team selection.
	Others?
Back to the Business
From a business perspective, customer segmentation divides a customer database into groups to provide a tailored customer experience - rather than offering single solution for everyone. 
The business value of creating such groups is the ability to implement specific business strategies, including:
	Customized promotions (e.g. special offers, discounts)
	Personalized communications (e.g. targeted marketing emails)
	Specific account policies (e.g. credit line)
 
The role of a data professional in driving business value lies in defining segments that are meaningful and aligned with business objectives.
Segmentation projects can be somewhat more open-ended and require analysts to think about the problem space from multiple points of view. Thinking deeply about business needs, customer behavior, and creative ways to apply various analytical tools makes segmentation a rewarding challenge.
🚀 With that in mind, let’s move on and get to know our stakeholder - the TravelTide company! 
 
________________________________________
 
The TravelTide Company
________________________________________
Welcome to TravelTide
E-booking startup TravelTide is a hot new player in the online travel industry. It has experienced steady growth since it was founded at the tail end of the COVID-19 pandemic (2021-04) on the strength of its data aggregation and search technology, which is best in class. Feedback from the customers has shown - and industry analysts agree - that TravelTide customers have access to the largest travel inventory in the e-booking space!
 
 Kevin Talanick, TravelTide’s CEO
 
Following the startup playbook, TravelTide has maintained a hyper-focus on building an unfair advantage along a limited number of dimensions - in this case, building the biggest travel inventory and making it easily searchable. Because of this narrow focus, certain aspects of the TravelTide customer experience are underdeveloped, resulting in poor customer retention. CEO Kevin Talanick is very motivated to retain and add value to existing customers with a Marketing strategy built on a solid understanding of customer behavior.
________________________________________
 
Meet Elena Tarrant, the new Head of Marketing. Elena has been brought on to supercharge the Marketing efforts at TravelTide. She is well known in the Marketing community as an expert in customer retention strategies, specifically rewards programs, an advanced feature proven to generate returns if executed well. 
 
 Elena Tarrant, TravelTide’s Head of Marketing
________________________________________
Elena’s mission is to design and execute a personalized rewards program that keeps customers returning to the TravelTide platform. It is difficult to personalize rewards for customers without first understanding them, so for the project to be successful, Elena will need to lean on the data team for customer insights.
 
Marketing 🤝 Data
________________________________________
You are on the Analytics team and responsible for supporting Elena’s rewards program project. Her subject matter expertise, together with your data skills, should result in a product reflecting marketing know-how and backed by solid evidence. After an initial meeting, Elena sent a follow-up message, reproduced here: 
 
 
Elena believes that to grab customers’ attention and maximize the likelihood, they will sign up for the rewards program, we want to emphasize the perk we think they are most interested in when we ask them to sign up.
Elena has also shared some mock-ups of rewards program invitation emails to give us a clear picture of the difference our analysis will make. 
 
 
 
The email on the right is vague and requires customers to read through a bulleted list of equally emphasized rewards. The one on the left has specific messaging about a free cancellation perk. Elena’s marketing logic is that if we believe a subset of customers will be particularly interested in free cancellation, TravelTide has a much higher chance of getting them to sign up for rewards using the email on the left. 
 
Our mission as Data Analysts is two-fold:
	First, we need to check if the data supports Elena’s hypothesis about the existence of customers that would be especially interested in the perks she is proposing.
	Then, for each customer, assign a likely favorite perk. 
So how will we tackle this task? This is what we are going to discuss next!
 
Approaching the Project
Project Time Structure in Detail
________________________________________
In each of the four weeks we will get one step further in our goal to help Elena and TravelTide! Let’s go over all 4 weeks now to see what exactly you are going to do:
1️⃣ EDA - Exploring the Data:
Familiarize yourself with the business context and available data. Use tools like SQL, Python, or even Google Sheets to understand the tables, the project, and its needs. Think about:
	customers to exclude from the analysis
	how to clean and prepare the data
	how to get the desired information through joining table or more complex CTEs/Python code. 
The outcome of this stage will be:
	a cleaned, filtered table at the session level
	a first aggregated table
	enriched table with the data about customers (users) with the level of granularity that is ready for the next stage of customer analysis
	a clear understanding of what each column of that table means.
2️⃣ Feature Engineering - Devising Metrics:
Think of the business case to identify key characteristics that can be used to characterize or group customers. Come up with combined columns that really capture interesting facts about our customers that may help us to group them. Then, you’ll need to get back to the session table and think of what aggregations can be additionally included for the users.
🐍 In the language of Data Analytics:
“Perform feature engineering to devise metrics or new attributes that are meaningful for segmentation.”
Think especially of how customers in the business of TravelTide differ from each other.
3️⃣ Customer Segmentation - Grouping the Customers:
Perform customer analysis using the created metrics. We want to find customer groups, understand them and find meaningful perks for members of each group. 
At this point you can use clustering methods to segment customers using machine learning and determine afterwards the meaning of the computationally found groups by exploring its members.
The outcome of this stage will be the assignment of all suitable customers into groups based on the segmentation criteria and an assigned perk that will suit them.
4️⃣ Presentation:
Create an executive summary and slides of the customer analysis results and record a video presentation. Describe the results of your analysis, including the info about the customer groups/clusters. Explain the characteristics of the customers within each group/cluster, such as their behavior, preferences, and other defining attributes. Give examples of group members as personas or directly from the dataset.
Find good visualizations (e.g.: bar plot, scatter plot, radar plot, etc.) to make your points and keep the attention of you audience. Use data storytelling principles to be convincing. 
Finally, include recommendations to the company on how to measure the success of your customer analysis in the upcoming months.
 
 
Familiarizing Yourself with TravelTide Data
 
Dataset
________________________________________
TravelTide stores its data in a relational database, which you can access here: 
 
Connect to the TravelTide database postgres://Test:bQNxVzJL4g6u@ep-noisy-flower-846766.us-east-2.aws.neon.tech/TravelTide
You can find a description of each table and its columns below: 
	users: user demographic information
	user_id: unique user ID (key, int)
	birthdate: user date of birth (datetime)
	gender: user gender (nominal)
	married: user marriage status (binary)
	has_children: whether or not the user has children (binary)
	home_country: user’s resident country (nominal)
	home_city: user’s resident city (nominal)
	home_airport: user’s preferred hometown airport (nominal)
	home_airport_lat: geographical north-south position of home airport (decimal)
	home_airport_lon: geographical east-west position of home airport (decimal)
	sign_up_date: date of TravelTide account creation (datetime)
 
	sessions: information about individual browsing sessions (note: only sessions with at least 2 clicks are included)
	session_id: unique browsing session ID (key, string)
	user_id: the user ID (foreign key, int)
	trip_id: ID mapped to flight and hotel bookings (foreign key, string)
	session_start: time of browsing session start (timestamp)
	session_end: time of browsing session end (timestamp)
	flight_discount: whether or not flight discount was offered (binary)
	hotel_discount: whether or not hotel discount was offered (binary)
	flight_discount_amount: percentage off base fare (decimal)
	hotel_discount_amount: percentage off base night rate (decimal)
	flight_booked: whether or not flight was booked (binary)
	hotel_booked: whether or not hotel was booked (binary)
	page_clicks: number of page clicks during browsing session (int)
	cancellation: whether or not the purpose of the session was to cancel a trip (binary)
 
	flights: information about purchased flights
	trip_id: unique trip ID (key, string)
	origin_airport: user’s home airport (nominal)
	destination: destination city (nominal)
	destination_airport: airport in destination city (nominal)
	seats: number of seats booked (int)
	return_flight_booked: whether or not a return flight was booked (binary)
	departure_time: time of departure from origin airport (timestamp)
	return_time: time of return to origin airport (timestamp)
	checked_bags: number of checked bags (int)
	trip_airline: airline taking user from origin to destination (nominal)
	destination_airport_lat: geographical north-south position of destination airport (decimal)
	destination_airport_lon: geographical east-west position of destination airport (decimal)
	base_fare_usd: pre-discount price of airfare (decimal)
 
	hotels: information about purchased hotel stays
	trip_id: unique trip ID (key, string)
	hotel_name: hotel brand name (nominal)
	nights: number of nights stayed at the hotel (int)
	rooms: number of rooms booked with hotel (int)
	check_in_time: time user hotel stay begins (timestamp)
	check_out_time: time user hotel stay ends (timestamp)
	hotel_per_room_usd: pre discount price of hotel stay per room per night (decimal)
 
What are the fact and dimension tables in the described DB schema? Think about this question for 2 minutes and make an argument for your choice before opening the Answer.Answer
	The sessions table is the fact table. Frequently updated and includes most granular information in this DB
	Users table is a dimension table that include additional information beyond user_id from the sessions table. This dimension table is connected to the fact table via the foreign_key ( user_id)
	Hotels and Flights are also fact tables as they don’t just include additional information about each hotel and flight but also have multiple rows per hotel/flight (one record/row per booking). They are frequently updated, new row every time a new booking is made. 
 
________________________________________
 
Initial Data Exploration
________________________________________
As with any data analytics task, before you dive into the complex EDA, start with simple steps. 🔔Note: You can use SQL, Python, or even Google Sheets for this task but using the combination of SQL and Python is strongly recommended! 
1. Understanding the Data Structure
Before diving into analysis, familiarize yourself with the database schema and understand how the tables are related. Check the size (number of rows) of all tables and pay attention to the data types of all columns. This understanding will help you in crafting meaningful SQL queries/Python codes.
2. Initial Data Quality Check
Perform initial checks to ensure data integrity. Check for null values and anomalies in different columns of a given dataset. Examine the unique values in different categorical columns. 
As an example, let’s have a look at the hotel_name column in hotels table by executing the below query. The question is: “Is there any convention of how hotel names are stored in this DB?”
 
 
As a result, it turns out that the hotel_name includes not just the name of the hotel but also additional information that might be useful to detect users who booked hotels in their home towns.
Find more such insights about the data at hand.
3. Descriptive Analysis
The next step in the descriptive analysis is essential to conduct.
Start by understanding the basic demographics of your user base. Continue to descriptive statistics of the hotel and flight bookings. Then move to the sessions table and explore the user behavior.
Possible exploratory questions in this section:
	Query the users table to get a breakdown of users by gender, marital status, and whether they have children. 
	What is the distribution of the user's birth year? Do you spot any irregularity there? What is special about birth year 2006? How would you calculate the age based on birth date?
	You may define “customer age” as a period in months since the user signed up to the platform. What is the average “customer age” of TravelTide user?
	What are the 10 most popular hotels? Include the information about the average duration of stay and average price before the discount. Do the same for most expensive hotels (top 10), hotels with the longest stays and etc. 
	Plenty of questions might be asked about the flight table. Just a few examples to ignite your creativity:
	What is the most used airline in the last 6 months of recorded data?
	What is the average number of seats booked on flights via TravelTide?
	What is the variability of the price for the same flight routes over different seasons?
Outro
By going over the suggested steps, you should familiarize yourself with the data at hands as well as get initial feeling about the next steps needed to be performed. And of the of the next steps that are logically valid is to preprocess the data, so let’s proceed with it!
 
Data Preprocessing
In the project stage that we are going to address now, you will familiarize yourself with the TravelTide rewards program and its business context. You will use appropriate tools to extract and explore the company database and form a plan for the next steps in customers segmentation.
🔔 Note: Again, feel free to use any tools for your analysis that you prefer.
 
🧑‍🎓 Good studying habits:
If you feel very frustrated at any point in your first read, please move on and continue reading the entire lesson. You might find answers to your questions later on in the lesson. 
And the very first step is to recap and define our objectives!
Objectives
________________________________________
	Filter TravelTide data using Elena’s (Head of Marketing) or your own cohort definition.
	Forming the initial extraction query which can be then used for further analysis in sheets or Python.
	Aggregate Session, Flight, and Hotel data to the appropriate level, preserving fields that carry demographic or behavioral data, and merge the results into a single table.
	Use an appropriate outlier definition to filter out extreme data points that might bias segmentation results.
Now, let’s go over each step and discuss it in details.
Filtering the data - Defining the Cohort
________________________________________
Which customers should we include in the analysis? This is an important parameter for segmentation analysis that was not explicitly mentioned in Elena’s initial message. 
 
First, let’s address the obvious question: why not all customers?
 
Recall the business context. We are trying to implement a rewards program (assigning perks) based on customer behavior. It takes time for behavioral data to pile up. Customers who signed up yesterday will have very few interactions with the platform. Including them in the same analysis as customers with months or years of platform interaction will skew results. This problem extends to comparing customers with 6 months on the platform vs 24 months on the platform, and so on. We need a way to control for the influence of time on platform. In Data Analytic terms, we need to select a cohort.
 
We will lean on Elena’s experience once again by asking her how she wants to define the cohort:
 
 
Visually, this is what Elena is suggesting:
 
💡
You are not limited to Elena’s recommendation. Think about different customer filters and explore a few different cohorts. Eventually, choose one that makes the most sense for you and continue your project with that cohort. 
Our data extraction query is starting to take shape:
 


How would you represent the cohort definition in the WHERE clause of a SQL query?Help
Video: filtering with multiple criteria (note: DataCamp will automatically take you to the next content block at the end of the video - but continuing is optional and only encouraged if you need extra practice)
 
 
Forming The Initial Extraction Query
________________________________________
Now that we’ve defined a cohort, we have limited our data to the customers we want to use for segmentation. The next step is to combine relevant data from across tables while getting the users from the defined cohort. 
Copied code
to clipboard
 
 
🤔
What kind of JOIN should we use?
Help
Video: Joining data
 
🤔
What is the aggregation level of the above query? Is it aggregated to the user level?
Help
Video: Data analysis with aggregations
 
As you remember, our goal is to get a session level data, but besides that, we may consider other aggregations, too. You may not be ready to aggregate to the customer level yet - perhaps you’d prefer to export session-level data to Python or other software for more exploratory analysis before aggregating, and that’s ok too - as long as you keep in mind that eventually, you need to aggregate to the customer level.
Your next step, if we talk about Python, would look like this:
 
You can then proceed with removing outliers and performing further EDA at the session level. We’ll talk about it later in this lesson.
Aggregate the data on user level
________________________________________
The extraction query is nearly complete, except for perhaps the most interesting part - the specific aggregation functions we utilize in the SELECT statement. Also, be mindful of the appropriate level of aggregation - this is a customer segmentation analysis.
To aggregate to the appropriate level of analysis (once we feel we have adequately explored session-level data), take note of the following:
	The primary key of each table
	Which fields carry information about behavior that might be relevant to our hypothesized perks?
We have many aggregation functions to choose from, endless ways to combine them, and complete discretion to make what we think are the most informative calculations.
Here is an example for SQL:
 and here is for Python:
  
At this point, we are more concerned with exploring the data than finding the optimal metrics to represent our target behavior. Start with simple aggregations while brainstorming more sophisticated ways to measure and combine variables in preparation for the rest of the analysis.
 
🤔
What fields should we aggregate and how? 
Video: Data analysis with aggregations 
⚠️
The initial stages of customer segmentation analyses are exploratory in nature. Segmentation is somewhat more open-ended compared to other types of analysis, giving analysts the freedom to exercise analytical creativity in defining metrics. It is expected that you will iterate over this and other queries many times as you dig into the problem.
Removing Outliers
________________________________________
Suppose you talk about this segmentation project with a ML Scientist. They might say, “Ah, you are trying to find clusters of typical values in the joint distribution of the data,” which roughly translates to grouping data points together if they behave the same on average along a bunch of different metrics. This is indeed what we’re trying to do, but the presence of extreme values might bias our estimates of average behavior.
  
 
Extreme values will skew the arithmetic average and other measures of central tendency and generally skew our perception of the data. 
 
Suppose we are given room service charge data, measured in dollars, for a handful of TravelTide customers. We might expect the typical hotel guest to charge a few meals to their room, and the initial batch of data we are shown reflects this:
  
The mean of this data is around $62, and the median is around $57.
 
Now imagine one of our customers throws a huge party in a Las Vegas penthouse, ordering the hotel's most expensive champagne. Let’s add this data point to our sample:
 
  
The mean blows up to $10,385. Notably, the median is much less affected, increasing by just a bit to $64.
 
In this example, it’s pretty easy to notice that one of the numbers is entirely out of proportion with the others. But TravelTide’s database is much more extensive than this, and we are certainly not going to inspect our dataset row by row to find extreme values. So how do we systematically check our data for outliers?
 
In most practical data analysis scenarios, we do not have a pre-set outlier definition. There’s no single universally accepted criteria for outliers, as it depends on the data context and perspective of the analyst. With that caveat in place, a common workflow for identifying outliers is first to visualize the data distribution, then decide on a threshold based on a measure of distance from the center of the distribution.
 
For example, suppose we have reason to believe the data follows a normal distribution. In that case, we can use a histogram and set an outlier definition equal to some standard deviations away from the sample mean. After observing the distribution on the left (below), we might decide to label any data point five standard deviations or more away from the mean as an outlier. Five standard deviations is a 1 in 500 million event under the assumption of normality, so we reason these data are pretty unlikely! 
 
 
🤔How do we translate “n number of standard deviations away from the mean” into a statement about the probability of an event?
Answer
 
 
If we don’t want to make any assumptions about the underlying data distribution, we can use a box plot to visualize the data and define outliers as points at least some number of IQR’s away from the data. 
🤔How do we interpret box plots - and what does IQR mean? 
Answer
	IQR stands for Inter-Quartile Range. It is calculated as the difference between the 75th percentile and 25th percentile of the data. Think of it as the range containing the “middle half” of the data.
	Reference: What is a Box Plot?
In the example below, we observe a skewed distribution using a box plot, and decide to define our outlier threshold at 5 times IQR. 
 
 
As we calculate metrics on TravelTide data (and do further calculations downstream in spreadsheets or Python), we’ll need to stay vigilant to the presence of outliers. However we decide to approach outliers, it is up to us to make sure we can articulate our thought process to technical colleagues and stakeholders.
 
🤔How many page clicks are there on average across all browsing sessions?Answer
 
Anomalies in the “Nights” column 
You might have seen rows where “Nights” column has invalid values, like: 
 
or
 
This might be disappointing, but as a future Data Analyst, you should start not getting annoyed by anomalies in your data. 
Okay, but what should you do then? 
There are two levels/steps to this question:
	What to do with those rows?
	The easiest approach would be to delete the rows with invalid values. Alternatively, you could find a way to determine the valid values and replace the 0s and negative ones with those. The second method prevents data loss, but how can you find the valid values? Is that even possible to do? This leads us to the second step.
	Why are those values there?
	Start thinking about the reasons behind this anomaly. Sometimes you can find reasons, but other times it might be impossible due to errors during data entry or data transformation. Understanding the cause can help you decide whether to fix or remove the data. 
Can check-in-time and check-out-time help us find the valid values?
As the analyst on the team, you will decide which approach to take. Keep or remove?
 
Ultimately, it's your call as the data analyst. You need to evaluate whether to keep or remove the anomalous rows based on the context and importance of the data. Always document your decision-making process and rationale for future reference and transparency.
 
________________________________________

Introducing the 2nd Project Week
Welcome back!
Recall that the business justification for creating customer segments is the ability to take segment-specific actions aligned with business strategy. It is absolutely essential to stay grounded in the strategic context your analysis is supporting, or else risk losing a meaningful connection between your work and the needs of the business.
☝️ As a reminder:
in this project, the business needs to segment customers based on affinity to rewards program perks.
What are we up to so far?
You now have quite valuable information about the customers! This is because in the previous step some metrics were defined and calculated. These additional calculations enriched our dataset and should help us in segmenting our customers in a better way, but how can we segment them?
This is exactly what we are going to talk about next! Our plan is:
1 Briefly recap the key segmentation algorithms in machine learning
2 Talk about dimensionality reduction techniques that may be helpful if ML methods are considered.
🚀 Let’s get started!
 
Segmentation Algorithms to Consider: K-means
As experts in machine learning, we definitely should consider the ML applications here to address the segmentation problem we are trying to solve. Let’s remind ourselves what is in our arsenal if we stick with the ML-based techniques. 
1️⃣ K-Means
________________________________________
One on the key algorithms that we typically consider when talking about segmentation is a distance-based approach like K-Means.
As you already know, K-Means belongs to a general class of Machine Learning algorithms called Unsupervised Learners.
As for the brief recap: under the hood the K-mean algo does the following:
	Generate K random points in the coordinate system defined by our behavioral metrics. Each of these K points represents the “center” of a segment.
	Calculate the straight line (Euclidean) distance between each customer and the K segment centers.
	Assign customers to the segment center they are closest to.
	Update the location of the segment centers to be the average of the customers that belong to them.
	Repeat steps 2-4 until the segment centers stop moving.

🤔Suppose we have two behavioral metrics, A and B, both on the scale 0-1. Then, we initialize K Means with K = 2. This means we want to find two segments. 
Step 1 of K Means randomly picks 2 locations in the space defined by our metrics, A and B, to represent the initial position of our 2 segment centers. 
Let’s say we have randomly initialized segment centers as shown below, and also two customers: 
 
 
Answer
Customers are assigned to the center they are closest to. “Closest to” means shortest Euclidean distance. As a reminder, here’s the formula:
 
Doing the math…we see that Customer 1 is closer to Center 1 than Center 2. So Customer 1 will initially belong to the segment that has Center 1 at its center. Which segment does Customer 2 belong to?
Given two behavioral metrics and K = 3 customer segments, here’s a visual depiction of K Means finding segments:

 

Let us challenge your intuition a bit now!
🤔How do you read the plot above to locate two behavioral metrics and three segments? What about customers - how are they represented in the plot?
Answer
The horizontal and vertical axes are the behavioral metrics. The blue, yellow and red color regions represent segments, and the data points (circles, x’s and +’s) are customers in each segment.
We will plug our data into K Means, specify K, the number of segments we want it to find, and then let the algorithm run.
🤔 What should K be if we run K Means to find customer perk segments?
Answer
K should be 5, because we want to find 5 perk segments.

As you already know, the k-means also is available in the sklearn library and its cluster module:
 

💬 Remember that:
Every clustering algorithms required for the data to be preprocessed! It means that all of the features must be numeric and scaled if needed.
 
Distance-based methods like K-Means are very powerful but have a significant limitation - the process of finding out what the segments actually mean happens after they have been formed. K-Means groups data in a bottom-up manner and requires us to conduct an analysis to discover the meaning of the segments after they’ve been found. 
💬 Another Important Reminder!
Clustering algorithms evaluation is typically performed by calculating the silhouette score! So, to assess how good or poor any clustering algo works, we typically stick with this metric.
What it means in essence is that K-Means and other distance-based methods require us to (mainly) rely on inductive reasoning to discover segment meanings. We say mostly because it’s possible to add constraints like the number of clusters you want to be found.
⛳ Call to action!
Use the K-means algo now to segment the TravelTide customers!
Even though it is worth trying K-Means, we know that there is another clustering algo that has advantages over K-mean, and this is DBSCAN that we are going to talk about next!

 
Segmentation Algorithms to Consider: DBSCAN
DBSCAN
________________________________________
DBSCAN is another ML-based powerful clustering algorithm, especially effective for identifying clusters of varying shapes and handling noise. Unlike K-Means, it does not require specifying the number of clusters in advance but instead groups points based on density.
The best way to illustrate the way it looks like is visually:

 
Look at how DBSCAN goes step by step and acquires (by making them yellow) more and more points that are near by the starting point.
 
Let’s Recap What DBSCAN Implementation Requires:
	Density-Based Clustering: Uses two key parameters:
	ε (Eps): Maximum distance between two points to be considered neighbors.
	MinPts: Minimum number of points required to form a cluster.
	Core, Border & Noise Points:
	Core points have at least MinPts neighbors within ε.
	Border points are within ε of a core point but lack enough neighbors to be core points themselves.
	Noise points are neither core nor border points.
DBSCAN starts from an arbitrary point, expanding clusters from core points while ignoring noise, and all of these together highlight the key advantages of this algo:
	Handles Arbitrary Shapes: Unlike K-Means, it identifies non-spherical clusters.
	Detects Outliers: Automatically labels noise points, making it useful for anomaly detection.
________________________________________
Choosing ε and MinPts
As we know from the previous experience, DBSCAN’s performance depends on selecting suitable ε and MinPts values, so it is essential to recap ho these two values needs to be set.
	Selecting ε
A k-distance plot (distance to the k-th nearest neighbor, where k = MinPts) helps determine ε. The "elbow" point—where the curve sharply changes—is a good starting choice.
 
	Selecting MinPts
A common heuristic is MinPts = 2 × number of features (columns), though dataset-specific tuning is often needed.
 
When both ε and MinPts , a high level implementation of a DBSCAN may look like this:
 
Conclusions
Now you are armed with two powerful clustering algorithms that you can use to approach the business need we have at TravelTide!
⛳ Call to action!
Use the DBSCAN algo now to segment the TravelTide customers! Compare the segmentation (clustering) results with what you got when employed K-means. Which algo does a better job? 
 
In the next lesson we’ll talk about further steps we may consider in this project which is dimensionality reduction.
 
Do we Really Need All Data? Let’s ask the PCA algo!
It may seem like either K-means or DBSCAN will do the job. Our goal should be achieved with one of them and the best algo is then selected, but is it really the case? What else can we do to make our solution more elegant? The answer is dimensionality reduction.
Brief Recap on Dimensionality Reduction
Let’s recap what we know about dimensionality reduction algos from our previous experience.
In essense, Dimensionality reduction techniques reduce the number of input variables (features) in a dataset while preserving as much information as possible.
Why do we need to think about it at this stage when we already trained clustering algorithms? Well, for a few reasons:
	Simplification: Fewer features make the data easier to understand and work with.
	Improved Performance: Fewer dimensions can lead to faster training and prevent overfitting in machine learning models.
	Visualization: Reducing high-dimensional data to 2D or 3D helps us create visualizations, making it easier to interpret complex datasets.
One of the most common dimensionality reduction method is PCA (Principal Component Analysis)
How Does PCA Work?
PCA is a linear dimensionality reduction technique that transforms your data into a new coordinate system where the axes represent directions of maximum variance (called principal components).
Let’s look at the below example:
 
Original two features shown as axes on the above image are S1 and S2:
	S1 is on the X axis and
	S2 is on the Y axis.
PCA algo found two new axes (aka components): PC1 and PC2 that best explain the variance in the data. This variance, as we see, is well captured by the two new components because the data varies the most along these two directions (components).
By finding the components that best explain our data, we can reduce the number of features (aka columns) in our dataset without loosing much of information.
Applying PCA
Here is how PCA can be imported and applied:
 
 
💬 Remember that:
the data that fit into the PCA algo must be preprocessed in a way that all of the features must be numeric and the numerical features are scaled.
Selecting the right number of components is vital. One approach on how to select it in a right way is to look at the cumulative explained variance and decide based on how much variance you want to retain.
Here's how you can plot the explained variance as a function of the number of components:
 
This plot helps decide how many components to keep based on the explained variance. You’ll usually want to choose the number of components where the explained variance starts to level off. In case of the plot provided, 2 components sound like a reasonable value.
Such a plot can be built using this Python code:
 
⛳ Call to action!
Try to reduce the number of dimensions in our original dataset and then try to cluster our customers again. Would be the results better of such an approach? It is worth finding it out!
Examining the Segments
Segments Identified. What’s Next?
By now, you should have successfully segmented customers using various methods - a process that was largely technical.
Once the segments are identified, it's crucial to analyze them further and uncover their unique characteristics. Understanding these distinctions can provide valuable insights for decision-making.
 
⛳ Call to Action!
Conduct Exploratory Data Analysis (EDA) to examine each segment independently. Identify their key traits - what makes each segment unique? How do they differ from one another? Use both numerical analysis and visualizations to uncover patterns. Finally, summarize your findings with clear conclusions based on your observations.
 
Crafting Your TravelTide Recommendations
Effective communication is a crucial skill for data analysts. Analysts may produce high-quality outputs, but failing to communicate findings clearly puts the output at risk of being ignored - or possibly worse, misunderstood. Remember that good communication allows your work to have the impact it deserves.

🤔In some cases, shortcomings in technical communication can put lives at risk. Can you think of examples of technical communication failures in Industry that had deadly consequences?
Examples
There are many examples. Here are a few of the better-known ones:
	The Challenger space shuttle disaster 
	The Ford Pinto - Ford's Pinto car model was infamous for a design flaw that could cause the fuel tank to explode in a rear-end collision. Ford engineers knew about this issue, but the way that they communicated it to management was through a cost-benefit analysis that showed it was cheaper to pay out potential lawsuits than to fix the problem. This cost-benefit analysis was miscommunicated and misunderstood at different levels within the organization, leading to a disastrous decision to continue with the production. Approximately 900 people died due to Pinto car explosions before production was discontinued.

There are many frameworks and templates for crafting effective communication products, but there are a few guiding principles to keep in mind.
Audience and Purpose
________________________________________
The structure, content, and tone of your communication all follow from knowing your audience and understanding the purpose of your work. Simply put, your purpose tells you what to communicate, and your audience tells you how.
 
Our audience is Elena, the Head of Marketing. Elena is a very competent marketer with a collaborative personality. She is in a very senior role at TravelTide, and as such has many demands on her time and attention.
 
🤔Is Elena really our sole audience?
Answer
Elena is our main focus for communication, but she is not the only focus. Technical colleagues are an important secondary audience. We communicate with them through comment blocks in SQL scripts, markdown in Jupyter notebooks, and other forms of documentation. In some cases, we may even write a comprehensive post showcasing the technical details of our analysis and publish it to the company intranet. We do this to create institutional knowledge, making ourselves and our teammates more productive.
Our purpose is to search for behavioral markers of 5 hypothesized rewards program perks and assign customers to each perk. From our audience and purpose, we derive the structure, content, and tone of our communication.

Our purpose is to search for behavioral markers of 5 hypothesized rewards program perks and assign customers to each perk. From our audience and purpose, we derive the structure, content, and tone of our communication.
 
	Structure: 
	Executive summary 
	5-minute slide presentation
	Content: 
	High-level takeaways tied to Elena’s initial ask
	Clear descriptions of identified segments
	Engaging visual(s) 
	Logical next steps
	Tone: 
	Non-technical
	Optimistic and forward-looking

 
🤔Why is it important to be optimistic and forward-looking?
Answer
It may seem like a strange thing to mention - but it is a common pitfall, especially amongst junior analysts, to fail to connect with their audience by telegraphing disappointment with the timeline, scope or general idea of the project they are presenting about. There is a time and place for discussing previously agreed upon project parameters, and during a slide presentation or in an executive summary is not it! 

Translate Technical Language into Intuitive Explanations
________________________________________
Avoid using jargon or complex technical terms that may confuse your audience. Use clear, straightforward language and everyday analogies to make your findings more understandable. For instance, instead of saying "a correlation coefficient of 0.9", you can say, "there's a strong relationship between X and Y".
 
Let’s consider our approach to finding customer segments via PCA and an unsupervised learning algorithm applied. Imagine how you would explain this metric to Elena….
One approach to avoid is repeating the technical definition directly. “I reduced dimensionality to 12 features and applied experiment with K-means clustering algo, finding the optimal number of clusters by assessing the silhouette score”. 
Accurate? Yes - but also dense, long, and full of jargon. 
 
Instead, boil it down to its essence without losing accuracy - “I identified clusters that our customers belong to and validated my approach by mathematically proving the defined segments” accomplishes this.

🤔Do we always need to avoid data jargon and technical explanations when communicating with executive stakeholders?
Answer
No - remember, communication strategy follows from audience and purpose. Many executives are former engineers or analysts who love quizzing junior colleagues on technical details. That’s a different kind of challenge!
 
Use Visuals to Communicate Key Findings
________________________________________
People process visual data far quicker than textual data, making visuals a powerful tool to communicate your key findings. Use visuals like bar, line, scatter, and other simple chart types to illustrate your points. Be mindful of the principles of good data visualization, including label clarity, proper use of color, and avoiding overly complex charts.
 
Let’s illustrate it visually. For instance, let’s consider an arbitrary column of data bud visualized differently: on the left there is an example of a bad plot, and on the right - there is a good and simple plot that does the job:
 
 
Not only is the plot on the left too cluttered, but it is also inaccessible to the 8% of the world population with red-green color blindness. In contrast, the histogram on the right is simple, and most people have seen one before, so it is unlikely you will need to review how to read the chart and can focus on pointing out essential takeaways from it.

 
🤔What’s another example of a chart type that is very popular among data professionals for visualizing the distribution of data that is typically more difficult for a non-technical audience to understand? Answer
A box plot. Simpler than a violin plot, but not simple enough. Box plots convey lots of useful statistical information in a compelling way - but require training and experience to interpret. Histograms or 1D scatter plots are common alternatives when a data distribution needs to be communicated to non-technical stakeholders.
	Refresher on principles of data visualization - Video: Effective Data Visuals

Specific Guidance on Additional Best Practices
________________________________________
Technical Communication
Regardless of how your workflow is divided, your technical work should be thoroughly documented, and key analytic decision points should be acknowledged and discussed. Without this level of technical communication, your work will not be reproducible, not even by you!
It’s good practice to annotate your files. Here’s a demonstration of the level of communication we expect using a SQL → Python workflow. 
For instance, we want to view how page_clicks grouped by number of flight seats booked varies over time, so we start with a SQL query:
 
In the SQL code above, we have a block comment explaining what the query is intended to do - this kind of block comment is useful for speeding up comprehension and debugging, especially in collaboration. We also include in-line comments explaining key syntax parts in the main SQL query.
 
Next, we bring the data over to Python to generate a plot. 
 

Similar to our SQL code block, we explain what we are doing and why, then provide supporting comments next to tricky syntax. We used a block comment here, but if you are using a medium like Jupyter Notebook, you are encouraged to put this kind of commentary in Markdown instead. Since we are providing lots of documentation, we can expect that even colleagues who are NOT Python users will be able to understand our work.

🤔The example above used SQL and Python. What if we used other tools, like Spreadsheets and Tableau, instead?
Addressing business questions
Recall Elena’s original ask:
 
 
 
A good deliverable will clearly state whether there’s evidence to support the perks Elena is proposing based on her subject matter expertise. If there is a misalignment between expectation and reality, it is important to understand that this is completely ok. 
 
You and Elena have just started a partnership to support the creation (and refinement) of an amazing rewards program. Now, we don’t expect Elena to be totally misguided, but if it turns out that the data only partially supports her hypotheses, it is your job to skillfully communicate this and make helpful suggestions as a data partner.
Answer
There are mechanisms in both Sheets and Tableau that allow you to add in-line and block comments to explain your thoughts and technical process to colleagues. The important thing is that you do it regardless of your software stack.
 
🤔What are some examples of ways to achieve only partial validation of Elena’s perk ideas? 
Ideas
	Due to a limitation of the data, behavior signals are inconclusive or ambiguous 
	There is redundancy between the perks (i.e. a pair of perks are so highly correlated that they may as well be one perk)
	There’s a behavioral pattern connected to a potential perk Elena did not think of!

Executive summary
Executive summaries are used to deliver important information to support decision-making. They should be concise and simple. They sometimes contain a centerpiece data visualization to visually illustrate a crucial point or insight. Here’s an example of how you might structure your executive summary:
 

To be clear - this is just one way to structure a report, NOT the only way. You can find plenty of other templates online. 
 
💡
As you synthesize your data analysis work for the business side, keep in mind the guiding principles of effective technical communication - audience and purpose, intuitive explanations, and simple visualizations.
This is the final but crucial phase of the project. Start by documenting your analysis files, and then create an executive summary and slides of the key results. Record a video presentation to practice your public speaking and interview skills.

All finished? 🥁
🎉
Congratulations!
Once you have compiled and documented your results, your project is complete. You’ve successfully become familiar with the TravelTide database in SQL, calculated metrics for the business context, segmented customer behavior, and communicated the key results. Great work!
 
roject Submission Guidelines
 
As mentioned in the previous lesson, you need to create an executive summary and slides of the key results, and record a video presentation to practice your public speaking and interview skills.
You’ll also need to submit links to your project files. 
🌟
You’ll need to submit your work by the end of the week, on Friday at max. 23:59h.
Project files
Start by documenting all the files related to your analysis. Ensure that your documentation is clear and well-organized.
Submit the Following Items:
	Link to the Project Folder: Provide a link to the folder containing all your project files. Ensure the folder includes:
Readme File: Create a Readme file using markdown. Consider Visual Studio Code with Markdown extensions, or, simply, Notion.
	
	
	
	
	
	
	
	

	CSV File: Include the CSV file with users assigned to the perks (rewards program).
	Folders with Code: Organize your code into folders. Example:
	/src: Source code
	/config: Configuration files
	/ipynb: Jupyter notebooks
	…
	(BONUS) GitHub Repository: Upload your project to a GitHub repository, including all your code, data, and documentation.
________________________________________
Project summary
Please submit a PDF file containing your project summary, which should include:
	Executive Summary – A concise, one-page executive summary.
	Detailed Report – An in-depth explanation expanding on the information presented in the executive summary (up to 3 pages).
For guidance on creating the executive summary, refer to the details provided in the previous lesson.
________________________________________
Video presentation
The video presentation will be focused on communicating your high-level results to company leadership. Remember that the audience is primarily non-technical. You should provide them with the necessary information to answer each business question, with your own reasoning clearly stated. The presentation should be carefully curated to tell a clear and compelling story.
Technical Guidelines:
	Record a maximum 5-minute duration video that demonstrates your outcomes. You can do it via Loom (a free account offers up to 5 minutes of recording time), Zoom, Youtube, or any other similar tool.
	The video presentation may use slides (Google Slides, Keynote, Microsoft PowerPoint).
	Share your screen and have an open camera to see the speaker.
Content Guidelines:
	You have a limited time to present your results (up to 5 minutes). Given that, the number of slides that you prepare should let you present your finding in that time frame. You should not dive into technical details too much. Tell the story with your data insights. However, highlight any irregularities in the dataset or caveats that the audience should be aware of when seeing your results.
	You can assume some facts that were not mentioned in the project description, just make sure to state your assumptions clearly.
	Use minimal content on your slides. You should not need more than 1-2 charts or more than six bullet points per slide. If you feel you need more, you probably need to add more slides.
Recommended Structure (Optional):
	Context: Give a very short overview of the customers. The stakeholders likely have an existing understanding, so you don’t need to explain much, but it is helpful to give a quick overview of which steps you are including in the funnel.
	Key Results: For each business question, explain the question at hand, your findings, and your recommendation.
	Conclusion: End the presentation by thanking your audience and perhaps reiterating 1-2 of the most important takeaways or recommendations.
 

