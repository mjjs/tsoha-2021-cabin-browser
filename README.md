# tsoha-2021-cabin-browser

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The application is a summer cabin browser for Finland. A cabin owner can list their
summer cabin on the site and customers can browse, rate, and book these cabins
for the summer.

A live demo is up at [https://cabin-browser.herokuapp.com/](https://cabin-browser.herokuapp.com).
The demo is running on Heroku free-tier, so it might take a while to start up if there have been
no visitors lately.

## Plan
The original plan can be found over at [plan.md](./docs/plan.md).

## Testing in Heroku
The application can be found [here](https://cabin-browser.herokuapp.com).
There are a few pre-made users that can be used when testing the application:

Customer:
* kalle.kayttaja@email.com : salasana

Cabin owners:
* olli.omistaja@email.com : salasana
* otso.omistaja@email.com : salasana

You can also register a new user if you want.

If you log in as a customer, you may:
* View the cabins that have been added by cabin owners.
    * Filter the cabins by keywords.
    * Filter the cabins by municipality.
* Book a cabin.
* Cancel a booking you have made.
* Review a cabin.
* Remove your added reviews.

If you log in as a cabin owner, you may:
* Add a new cabin to the site.
    * Add custom keywords for the cabins during cabin adding process.
* Remove your cabins from the site.
* Delete any spam reviews from your cabins.
