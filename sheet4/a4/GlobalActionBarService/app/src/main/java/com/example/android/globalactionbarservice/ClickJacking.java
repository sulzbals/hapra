package com.example.android.globalactionbarservice;

import android.view.MotionEvent;
import android.view.View;

public class ClickJacking implements View.OnTouchListener {
    private final Runnable mCallback;

    public ClickJacking(Runnable callback) {
        mCallback = callback;
    }

    @Override
    public boolean onTouch(View v, MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_OUTSIDE) {
            mCallback.run();
            return true;
        }
        else {
            return false;
        }
    }
}
