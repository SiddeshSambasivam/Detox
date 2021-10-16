package com.example.deeptox;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import android.graphics.PixelFormat;
import android.view.WindowManager;
import android.widget.LinearLayout;


//service to call overlay activity
public class OverlayService extends Service {

    LinearLayout oView;

    public OverlayService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    //set overlay configurations
    @Override
    public void onCreate() {
        super.onCreate();
        oView = new LinearLayout(this);
        oView.setBackgroundColor(0x17170432); // The color
        WindowManager.LayoutParams params = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                0 | WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
                PixelFormat.OPAQUE);
        WindowManager wm = (WindowManager) getSystemService(WINDOW_SERVICE);
        wm.addView(oView, params);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if(oView!=null){
            WindowManager wm = (WindowManager) getSystemService(WINDOW_SERVICE);
            wm.removeView(oView);
        }
    }
}