package com.example.deeptox;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.toolbox.StringRequest;

import java.util.HashMap;
import java.util.Map;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

public class MyAccessibilityService extends AccessibilityService {
    private static final String TAG = "MyAccessibilityService";

    //endpoint URL for our deep learning model, deployed in AWS
    private String url = "http://ec2-13-212-167-131.ap-southeast-1.compute.amazonaws.com/api?sent=";


    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        AccessibilityNodeInfo mNodeInfo = event.getSource();
        checkOffensive(mNodeInfo);
    }

    //code to get all the text on the current screen
    //and pass it to our deep learning model via the endpoint url
    private void checkOffensive(AccessibilityNodeInfo mNodeInfo) {
        int mDebugDepth = 0;
        if (mNodeInfo == null) return;
        String log ="";
        for (int i = 0; i < mDebugDepth; i++) {
            log += ".";
        }

        Intent inte = new Intent(this,OverlayActivity.class);
        inte.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

        if (mNodeInfo.getText() != null) {
            String replaceString=(mNodeInfo.getText().toString()).replace(" ","%20");
            Log.e(TAG, "checkOffensive:  " + url+replaceString);
            StringRequest stringRequest = new StringRequest(Request.Method.GET, url+replaceString,
                    new Response.Listener<String>() {
                        @Override
                        public void onResponse(String response) {
                            try{
                                //open overlay if offensiveness score greater than 0.8
                                response += response.substring(response.indexOf(":") + 1, response.indexOf(","));
                                float response_float=Float.parseFloat(response);
                                if (response_float > 0.7) {
                                    startActivity(inte);
                                }
                            } catch (Exception e){
                                e.printStackTrace();
                            }
                        }
                    },
                    error -> Log.e("ERROR", "" + error.getMessage()));

            RequestQueue requestQueue = Volley.newRequestQueue(MyAccessibilityService.this);
            requestQueue.add(stringRequest);
        }

        log+="("+mNodeInfo.getText() +" <-- "+
                mNodeInfo.getViewIdResourceName()+")";
        Log.d(TAG, log);
        if (mNodeInfo.getChildCount() < 1) return;
        mDebugDepth++;

        for (int i = 0; i < mNodeInfo.getChildCount(); i++) {
            checkOffensive(mNodeInfo.getChild(i));
        }
        mDebugDepth--;
    }


    @Override
    public void onInterrupt() {
        Log.e(TAG, "onInterrupt: something went wrong");
    }

    @Override
    protected void onServiceConnected() {

        super.onServiceConnected();
        AccessibilityServiceInfo info = new AccessibilityServiceInfo();
        info.eventTypes = AccessibilityEvent.TYPES_ALL_MASK;

        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_SPOKEN;


        info.notificationTimeout = 100;

        this.setServiceInfo(info);
        Log.e(TAG, "onServiceConnected: ");
    }
}