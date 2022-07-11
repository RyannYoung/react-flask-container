# Quick-Start How to

Most of the project should work out of the box follow the steps to startup each individual element

## Pre-start (Initialise the Python virtual environment)

You'll need to open a terminal window in the python virtual environment (venv). To do this open a new terminal window and open

```
venv/Scripts/activate
```

This will be a `.bat` file which will open your terminal session into the python venv

## Backend API

Open the terminal window to `backend` and run

```
flask run
```

## Frontend UI

Open the terminal window to `frontend` and run

```console
npm i
npm start
```

## Scraper (Scraping Utility)

Scrapy is configured to utilise 3 spiders:

- Generic: A basic spider for static html pages (not dynamically loaded). This spider demonstrates how to select specific elements, and output data to a folder (_exports/generic_)
- Dynamic: Utilises Microsoft Playwright to create a live web environment to render dynamic webpages, this additionally support **full page screenshots** and **PDF document exports**. This spider demonstrates how to dynamically load a webpage by utilising a middleware to intercept the request and route through Playwright.
- Image: Utilises the in-built Image downloading pipeline to download all images on the webpage.

To run these spiders open the terminal window to `scraper`

```
scrapy crawl <spider_name> (generic/dynamic/image)
```

# To-do

- Create a docker-file of this project
- Create the scrapy daemon to link scrapy to the backend
