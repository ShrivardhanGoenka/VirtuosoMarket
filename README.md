# ViruosoMarket

VirtuosoMarket is an online free-of-cost paper trading platform. People who are new to the market can learn the ropes of the market by gaining first hand experience in a completely safe and risk free way.

## Overview

This web application is made using the Django framework. It uses HTML, CSS, Bootstrap 5, JavaScript and JQuery for the frontend. 
SQLite is used for the database. All the data is kept encrypted using the Django encryption system.
The web application uses a library called [nsetools](https://nsetools.readthedocs.io/en/latest/) which fetches data directly from the National Stock Exchange of India with a lag of 1 second.

The first version of the paper trading platform will have the following features:
- Navbar with the following options:
  - When not signed in: 
      - Sign in
      - Sign Up
      - About
      - Home Page (brand logo)
      - View Stocks
  - When signed in:
      - My profile
      - Log out
      - Contests
      - About
      - View Stocks
      - Home Page (brand logo)
      - My Portfolio
- Sign in, Sign out, and Log out will be standard pages.
- ‘About Page’ will be a standard page.
- ‘My Portfolio’ will have the following features:
  - Users can check their current holdings in the currently used portfolio.
  - If the user is currently in a competition, it will also display the leader board of the competition and the user’s ranking in the competition.
  - There will also be a ‘My orders’ section which will display all the active orders at that point of time. 
  - In the list of all the stocks, the user may go to any stock (in the ‘view stocks’ template by just clicking the name of the stock.)
  - At the end there will be a log/ order history which will show all the requests made by the user (pending, executed, active). 
  - In the leader board, there by clicking on the username, the author may also go to that person’s profile. Any person’s profile viewed by another user’s profile will display the following information:
      - The username, and bio
      - The contests the user is present in.
- ‘View Stocks’ will have the following features:
  - There will be a search bar which allows the user to search for stocks based on name and ticker symbol. 
  - There may be a graph provided (subject to availability of data)
  - An option to trade the graph will be given if the user is signed in. The trade will be made in the portfolio the user is currently using (for more information please refer to the points on the contests)
  - The types of trading provided are provided in a separate point.
  - The stocks will provide the following information:
      - Exchange traded in (if multiple exchanges are added)
      - The current price (which will be updated in a certain number of seconds which will be decided later)
      - The last close price, the change (real and percent), 52 week high/low, the volume traded.
      - If the market is closed at that time, there will be a message displayed that the market is closed as well.
-‘Contests’ will have the following features:
  - Contests the user is part of
  - Option to switch between contests for portfolio
  - On the navbar, while hovering over the navbar, the current contest the author is currently trading under will be displayed. An individual option will also be provided
  - A search bar will be provided to search for contests and accordingly the user will be allowed to join new contests (depending on whether the contests searched for is public or private).
  - An option to create a new contest will also be provided. In any contests the user creates, the user will be given access to choose whether it is public or private, will have the option to remove players based on inappropriate behaviour (However, the user will be required to give an adequate reason to remove players if they report it as unethical to the administration).
- ‘My profile’ will have the following options:
  - Display the username, email address, name, and bio
  - Bio is changeable
  - Change Password option
  - All the leagues the person is part of.
- Buy/Sell: The following options for buying and selling will be provided:
  - Buy at market value: The user is purchasing the stock at the current market price
  - Limit Buy: The user can select a certain price below the current price and if the price of the share becomes less than or equal to that price then the system will purchase the share at the price. This offer will only be valid for the next 3 business days(days when the market is open).
  - Stop Loss: The user will be allowed to set a price below the current value and if the stock drops to or below that price then the system will automatically sell all the shares to prevent further loss. 
  - Target: If the stock touches a value above the current market price(when prescribed by the user), then the system will sell all the shares to collect the profit.

## Availability

Due to high costs of maintenance and upgrading to a higher version, this project has currently been taking down. Any inconvenience is regretted.

## Usage

To run this project locally, all of the above libraries need to be downloaded using the 'pip install' command in the terminal/ cmd.
Some fields are left empty due to security reasons, and thus, they need to be filled as without them, the application may not run. They are the Django Security Key and my Email SMTP details. Both of these details are available on the settings.py file in the Main folder.
To run this project the following command needs to be entered in cmd/ terminal. The path should be in the top level directory and all the packages must be installed and the virtual environment(if used) should be activated

```bash 
python manage.py runserver
```
More information about using custom ports and IPs can be found on the [Django documentation](https://docs.djangoproject.com/en/3.2/intro/tutorial01/#the-development-server)

## LICENCE

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



Source: [MIT Licence](https://choosealicense.com/licenses/mit/)
