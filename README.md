# tsoha-2021-cabin-browser

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The application is a summer cabin browser for Finland. A cabin owner can list their
summer cabin into the site and regular users can browse, rate, and book these cabins
for the summer.

A live demo is up at [https://cabin-browser.herokuapp.com/](https://cabin-browser.herokuapp.com).
The demo is running on Heroku free-tier, so it might take a while to start up if there have been
no visitors lately.

## Plan
The original plan can be found over at [plan.md](./docs/plan.md).

## State of the project
The project is almost completely finished. There are some finishing touches I want to do to it, but other than that, I think it's ready.

## Testing in Heroku
The application can be found [here](https://cabin-browser.herokuapp.com). There are a few pre-made users that can be used when testing the application:

Customer:
* kalle.kayttaja@email.com : salasana

Cabin owners:
* olli.omistaja@email.com : salasana
* otso.omistaja@email.com : salasana

You can also register a new user if you want. You can browse the cabins and add reviews/reservations to cabins as a customer. If you log in as a cabin owner, you can add new cabins also.

## TODO
* Fix image links
  * In a real application I would store the images on disk or in an S3 bucket. S3, however, might be overkill for a school project and Heroku clears all disk files on restart.
* Add timestamps to reviews
* Refactor code
