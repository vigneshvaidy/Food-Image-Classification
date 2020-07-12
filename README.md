# :fork_and_knife: Food Visualizer :fork_and_knife:

![Logo](/Dashboard/SeeFood/assets/img/brand/food-logo.png)

This Project helps in classifying food items and obtain nutritional insights , restaurant and recipe recommendations.All of this is 
facilitated through the react native application which works on both android and ios

## Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Getting Started](#Getting Started)
    * [Prerequisites](#prerequisites)
    * [deploying](#deploying)
- [Tech Stack](#techstack)
- [Visualizations](#visualizations)
- [Summary](#summary)
- [Future Work](#future Work)
- [Acknowledgments](#acknowledgements)
- [Authors](#authors)

## Introduction

The user can interface through the app where he/she can take a picture/Choose an image from the gallery and then a prediction for the food is made, once that is done, we can get nutritional insights, restaurant and recipe recommendations on the dashboard.

We can see the architecture diagram of the entire system below:

![architecture](/Output/Architecture.png)

## Demo

<p align="center"><img alt="logo" src="/Output/demo.gif"></p>

You can download the app by clicking this [link](https://expo.io/@sammyboi/seefood)

## Getting Started

### Prerequisites

install **node package manager**

```bash
pip install npm
```

install **expo-cli**

```bash
npm install -g expo-cli
```

install **firebase**

```bash
npm install -S firebase
```
### Deploying

We use flask and app engine to deploy the website

**setup google app engine**

install gcloud from this [link](https://cloud.google.com/sdk/docs/)

After installing gcloud we need to setup app engine

```bash
gcloud components install app-engine-python
```

**setup Third party libraries**
    
we run this command inside the dashboard folder

```bash
pip install -t lib -r requirements.txt
```

## Tech Stack
- **App Development**
    * [expo](https://docs.expo.io/versions/latest/) (React Native)
    * [Google Vision API](https://cloud.google.com/vision/)
    * [Google Firebase](https://firebase.google.com/)
- **Dashboard**
    * [Google App Engine](https://cloud.google.com/appengine/)
    * [Google Cassandra Cluster](https://console.cloud.google.com/marketplace/details/google/cassandra)
    * [Flask](http://flask.palletsprojects.com/en/1.1.x/)
    * [Jinja2](https://www.palletsprojects.com/p/jinja/)
    * [Google Maps API](https://developers.google.com/maps/documentation)
    * [Chart.js](https://www.chartjs.org/)
    * [Bootstrap](https://getbootstrap.com/)

## Visualizations

We get insights for nutrients and recommendations for recipe and restaurants, We can see sample output for **pizza** below

#### Nutrients insights 

**insights for nutrients**
![nutrient](/Output/nutrient.jpg)

**insights on calorie values**
![calorie](/Output/calorie.jpg)

**insights on food fat**
![fat](/Output/fat.jpg)

#### Restaurant Recommendation

![restaurants](/Output/restaurant.jpg)

#### Recipe Recommendation

![recipes](/Output/Recipes.png)

## Summary

So as we can see, given an image of any food item, we are able to classify the food item. Once the item is classified, we make 3 **GET**
requests to our dashboard, where we pass the food label name, the dashboard receives this food label and does the following 3 tasks
- Query Cassandra with the food label to get nutrients information
- Query Cassandra with the food label to get top rated restaurants information
- Scrape recipe data for the identified food label

Once we receive data from cassandra to our dashboard, we then pass these values to our visualizations through jinja which is a template engine
We can then view all our visualizations in one place.

## Future Work

We are planning to add support for user profiles in order to store previous data. We can see the previously scanned images and also the insights related to that.
That way a user can lead a better life by making healthy life choices :smiley:

## Acknowledgements

- [react-native app](https://github.com/JscramblerBlog/google-vision-rn-demo)

## Authors

- Sameer Pasha
- Archana Subramanian
- Ravi Kiran Dubey
- Vignesh Vaidyanathan