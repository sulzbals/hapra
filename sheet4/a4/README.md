#   A11y & Overlays (Aufgabe 4)

The app contains the Global Action Bar accessibility service (which is the example one from Android webpage), and the main activity consists of opening the accessibility settings and covering it with overlays. The goal is luring the user into:

1. Clicking on the Global Action Bar service, displayed on the list of accessibility settings and
2. Clicking on the switch that enables the service.

The overlay screens are built by accessing the layout resources I have defined and dimensioning it appropriately. All views are set as non-clickable, except for the one that we want the user to click, so if there is a click anywhere outside this region we want to lure the user into clicking, it is not sent to the activity running behind the overlays. This excludes the possibilities of enabling another service, or not enabling anything at all, for example.

I spent a lot of time trying to figure out a way to overlay the dialog that asks permissions for the accessibility service, as it was always brought to front while the overlays I have built stayed in the background. I did not find a way to do it, so the app just overlays the first two screens until this dialog is shown.

I left some commented code lines on `Overlay.firstScreen` and `Overlay.secondScreen` that can be used to build transparent overlays, where the clickable regions are transparent red and the non-clickable ones are transparent blue, so one can see exactly what the user is lured into clicking.

I did all the tests with the image `4 WVGA (Nexus S) API 24`. The dimensions of the views should be right for a clean install in an emulator running this image.