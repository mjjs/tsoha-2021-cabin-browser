# tsoha-2021-cabin-browser

The application is a summer cabin browser for Finland. A cabin owner can list their
summer cabin into the site and regular users can browse, rate, and book these cabins
for the summer.

## Functionality
### Users
A user of the site can register a new username. The user can either register as
a regular user (customer) or a cabin owner. The application also has a single
admin user that will be created during application initialization.

#### Cabin owner
A cabin owner can add/remove their cabin(s) from the website.

#### Customer
A customer can browse the cabins and reserve it for given days. The customer can
also leave reviews about the cabins.

#### Admin
An admin can delete users, cabins, and reviews if necessary.

### Cabins
#### Cabin adding
When adding a cabin to the website, the cabin owner can supply the following 
information about it:
* name
* location
* description
* price (€/day)

The cabin can also be added under labels such as "sauna", "lake", etc.

#### Cabin listing
The cabins are shown as a list to the user. The list can be filtered by municipality
and labels. The list can be sorted by price or review score.

#### Detailed info page
When a cabin is clicked in the list view, the user is taken to a detailed information
page of said cabin. The page shows all the information that the cabin owner has
entered plus all the reviews from the other customers. New reviews are able to be
left from this page as well.

From the info page, the customer can select dates and reserve the cabin if it's
available.
