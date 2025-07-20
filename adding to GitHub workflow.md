# Adding docu-lite to your GitHub workflow
I have just been through this process on this repository, so that I get the same user experience as anyone using docu-lite.

Here's how to ensure that you create an up to date outline on every commit.

### Create a file called something like this (the name doesn't matter, but the file location does):
   ```
   your-repository/.github/workflows/update_overviews.yml
   ```
   Here's mine: [update_overviews.yml](https://github.com/G1OJS/docu-lite/blob/main/.github/workflows/update_overviews.yml)

### Ensure that you have read/write permissions set for your actions
Go to the repository settings:
![menu](https://github.com/user-attachments/assets/13fbf693-dd58-4f8d-ac47-a04123870388)

Then, on the side bar:

![Capture](https://github.com/user-attachments/assets/fdf629da-33a0-4f3d-8ac8-1a018b3a2a81)

Finally, on the bottom of the page
![perms](https://github.com/user-attachments/assets/67e10ad9-1f45-41de-82af-ed6d7ab3f279)





