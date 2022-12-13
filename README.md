Inspired by: [Sleepingpirates/Invitarr](https://github.com/Sleepingpirates/Invitarr), [Jellayy/Invitarr](https://github.com/Jellayy/Invitarr)
<br>
PlexFriends is a discord bot that automates and manages inviting users in a Discord server to a Plex server.

## Sections
- [Features](#features)
- [Installation](#installation)
  - [Register your Discord Bot](#register-your-discord-bot)
  - [Deploy to Docker](#deploy-to-docker)
  - [Configure](#configure)
  - [Personalize your messages](#Personalize-your-messages)
- [Usage](#usage)
  - [User commands](#user-commands)
  - [Advanced commands](#advanced-commands)
- [Questions - Answers](#questions-answers)
- [Changelog](#changelog)

## Features
PlexFriends can:
 - Connect a server and a Plex account (1 bot => 1 Plex server)
 - A role to subscribe / unsubscribe a member on the Plex server
 - A role per library to authorize only certain libraries of the Plex server
 - Store user information in a local file (avoid asking again for the email address if we already know it)
 - Create Overseerr accounts for invited users to send requests (Optional)
 - Send a personalized private welcome message (Optional)
 - Management of a trial period of a configurable duration for people (Optional)
 - Customizable messages (English by default, Optional)
 - Subscription management with DonateBot (Optional)

## Installation

### Register your Discord bot
1. Create a bot on the [Discord Applications page](https://discord.com/developers/applications)
2. Make sure your bot has access to the `GUILD_MEMBERS` intent
3. Declare your bot as `bot` and the rights as `administrator`

### Deploy to Docker

#### Docker Compose

```
version: "2.1"
services:
  plexfriends:
    image: paloindici/plexfriends:latest
    container_name: plexfriends
    environment:
      - TZ=Europe/London
    volumes:
      - /path/to/data:/config
```

#### Docker CLI

```
docker run -d \
  --name=plexfriends \
  -e TZ=Europe/London \
  -v /path/to/data:/config \
  paloindici/plexfriends:latest
```

Note: It is recommended to omit any restart policy until you have populated your config.json file. After finishing the setup process, feel free to change 'restart' to 'unless-stopped'

### Configure
1. Run the bot once to generate an empty config.json file in the /config directory
2. Configure the `config.json` file:

```
{
  "bot_token": "xxx",
  "guild_id": xxx,
  "private_channel_id": xxx,
  "role_subscriber": "Subscriber",
  "plex_user": "xxx@xxx.xxx",
  "plex_password": "xxx",
  "plex_url": "https://xxx.xxx",
  "plex_token": "xxx",
  "overseerr_url": "https://xxx.xxx",
  "overseerr_api_key": "xxx",
  "test_duration": 24,
  "donate_api": "xxx"
}
```

Assuming you have configured everything correctly, PlexFriends will send DM invites to any user that receives the configured subscriber role if it is unknown to the database. Make sure your users have their DMs open!

---

To get `guild_id` and `private channel_id` you need to enable the developer mode. To do this, go to user settings, Advanced, and activate developer mode. Next :
- For `guild_id`, right click on the server icon, then copy the identifier
- For `private channel_id`, right click on the chosen channel, then copy the identifier

---

If you don't want feedback in a private channel, leave the private_channel_id field at 0: `"private_channel_id": 0`

If you don't want to use Overseerr, leave the overseerr_url field empty: `"overseerr_url": ""`

If you want to disable the trial period feature: `"test_duration": 0`. Otherwise, enter the duration of the trial period in hours.

If you don't want to create a subscription system with DonateBot: `"donate_api": ""`

All other fields in the config.json file are required

### Personalize your messages

By default, generic messages in English are sent. You can configure all messages in your language, or more personalized.

Some tips for your messages:
- `\n`: Go to line
- `[click here](https://www.link.com)`: Displays only 'click here' and redirects to the page if clicked
- `__text__`: Display 'test' will be underlined
- `**text**`: Display 'test' will be in bold
- `<member>`: Replace `<member>` with the name of the concerned member. (Only for `private_new_trial`, `private_new_subscription`, `private_end_subscription`)


Create a `language.json` file in the `/config` volume and paste the following block of text
```
{
  "ask_for_email": {
    "title": "Plex Share Invite",
    "message": "Please provide your Plex account email address to be invited to share, by replying to this message.\nThis request will expire in 1 hour"
  },
  "email_success": {
    "title": "Invite Sent",
    "message": "Check your Plex account for a friend request.\nA welcome message with important information will be sent to you by private message"
  },
  "invalid_email": {
    "title": "Invalid Email Provided",
    "message": "Please reply with a valid email address"
  },
  "email_timeout": {
    "title": "Plex Invite Timeout",
    "message": "No valid email was provided within 1 hours, please contact a server administrator to be re-invited"
  },
  "email_in_use": {
    "title": "Email In Use",
    "message": "This email is already in use by another user on this server, please contact your administrator"
  },
  "dm_cancelled": {
    "title": "DM Cancelled",
    "message": "Your registration has been canceled"
  },
  "delete_account": {
    "title": "Access delete",
    "message": "Your access to the Plex server has been removed"
  },
  "delete_account_admin": {
    "title": "Access delete",
    "message": "This user has been removed"
  },
  "database_content": {
    "title": "Database content",
    "message": "Member name - Member id - Member email\n\n"
  },
  "welcome_message": {
    "title": "Welcome !",
    "message": "Welcome to **Plex**!\nFor any questions, you can contact me on Discord\n\nGood viewing !"
  },
  "trial_in_progress": {
    "title": "Preparation for trial period",
    "message": "Preparation for the trial subscription... Please wait..."
  },
  "end_trial": {
    "title": "End of trial subscription",
    "message": "The trial period is over. If the content has you more, you can take out a subscription."
  },
  "already_tested": {
    "title": "Already tested",
    "message": "You have already tested the subscription for free. You cannot test more than once."
  },
  "never_tested": {
    "title": "Never tested",
    "message": "This user never did the trial period"
  },
  "unauthorized": {
    "title": "Unauthorized",
    "message": "You do not have permission to use this command. Administrator only"
  },
  "launch_trial": {
    "title": "Launch trial period",
    "message": "Launch of the trial period.\nWatch your discord private messages !"
  },
  "not_in_db": {
    "title": "Not in Database",
    "message": "This user is not in the database"
  },
  "reset_trial": {
    "title": "Trial period reset",
    "message": "Trial period for this user has been reset"
  },
  "confirm_send_welcome": {
    "title": "Success !",
    "message": "The welcome message has been sent"
  },
  "subscription_in_progress": {
    "title": "Subscription",
    "message": "Subscription request taken into account.\nGo to your private messages to continue!"
  },
  "subscription1": {
    "title": "Subscription",
    "message": "To start, you need to choose the Plex libraries you want to have access to."
  },
  "subscription2": {
    "title": "Subscription",
    "message": "To take out a new subscription, click [here](https://yourDonateUrl.me)"
  },
  "select_lib_timeout": {
    "title": "Library Select Timeout",
    "message": "You took too long to respond. Start your subscription request again"
  },
  "current_subscriptions": {
    "title": "Current Subscriptions",
    "message": "User - End Date\n\n"
  },
  "pre_end_subscription": {
    "title": "Subscription coming to an end",
    "message": "Your Plex subscription is about to expire in 2 days.\nRenew it now to keep access."
  },
  "end_subscription": {
    "title": "Expired subscription",
    "message": "Your Plex subscription has expired."
  },
  "private_new_trial": {
    "title": "New trial subscription",
    "message": "New trial period request for <member>"
  },
  "private_new_subscription": {
    "title": "New monthly subscription",
    "message": "New monthly subscription for <member>"
  },
  "private_end_subscription": {
    "title": "End of monthly subscription",
    "message": "End of monthly subscription for <member>"
  }
}
```

## Usage

Several roles are created in the Discord server:
 - A role for the subscriber - `BotName - role_subscriber`
 - One role per library of your Plex server - `BotName - LibrairieName`

Most logical procedure
 - Select the library roles to share with the member
 - Select subscriber role
 - If the member is unknown to the database, a private message is sent asking for their email address from their Plex account.
 - Once the email address is known, a friend request is sent to it, the Overseerr account created (if overseerr_url has been filled in config.json) and a private welcome message (if welcome_message has been filled in config.json)

If the member is in Plex friends, shared libraries are updated by changing library roles.

Please note: if the friend request is pending acceptance, the library roles cannot be changed. You must wait for the member to accept the friend request.

### User commands 

`/trial_subscription` Request a trial for the time-limited Plex subscription.

`/subscription` Get a 1 month subscription to Plex

### Advanced commands 

PlexFriends uses slash commands. Type / in a room to see the commands displayed.

All these commands are accessible only for the administrator

`/delete_user <@member>` Removes a given user from plex shares and deletes their associated Overseerr account if available.

`/delete_user_by_email <e-mail>` Removes a given user by email (if the user is no longer on the discord server) from plex shares and deletes their associated Overseerr account if available.

`/get_db` See the contents of the bot database.

`/send_welcome_message <@member>` Force the sending of the welcome message to a selected member

`/view_all_plex_friends` Display the complete list of Plex friends, and if they are present in the bot's database

`/reset_trial_subscription <@member>` Reset a member's trial period

`/preview_message <message_name>` Preview any message. All message names are offered in a list. Type the first letter to filter

`/gift_subscription <@member> <limited_time>` Offer a subscription to a member within a time defined in hours

`/current_subscriptions` See current subscriptions and their end date

## Questions - Answers

Q - Why when I give a role to a person, the role removes itself ?

A - If the friend request on Plex is pending acceptance, the bot cannot modify the shared library of this friend. Retry once the request is accepted.

---

Q - If I delete all library roles, does the subscriber role delete?

A - It's normal. The Plex API does not allow remaining friends in a shared library. It is therefore removed from friends.

---

Q - When I click on the subscribed role, it withdraws. Why ?

A - You can't be friends without a shared library. First select the shared library, then give it the role of subscriber.

---

Q - How can I see the rendering of my welcome message ?

A - Use the command /send_welcome_message and section your name to send it to yourself by private message

## Changelog

`v0.0.1`
- Starting the project

`v0.0.2`
- Fix bugs
- Added command to list all Plex friends

`v0.0.3` 
- Added a function to manage a member's free trial period (which he requests himself)

`v0.0.4`
- Added a command to reset a member's trial period
- Added an error message if a non-admin member tries a command that should be admin

`v0.0.5`
- Added ability to customize messages
- Preview any message
- Offer a subscription to a member within a defined time

`v0.0.6`
- Fix bugs

`v0.0.7`
- Setting up help messages in slash commands
- Added bot status with version

`v0.0.8`
- Fix bug with messages encoding

`v0.0.9`
- Monthly subscription management (Payment via Donate Bot)

`v0.0.10`
- Messages are made private to whoever requests it.
- Activation of the return to a private channel if activated for trial periods, new subscriptions and end of subscriptions

`v0.0.11`
- Fix bugs

`v0.0.12`
- Fix bugs for /delete_user command

`v0.0.13`
- Fix bugs for /trial_subscription command