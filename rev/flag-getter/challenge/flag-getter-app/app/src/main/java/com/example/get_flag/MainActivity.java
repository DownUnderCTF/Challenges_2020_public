//i clearly have no idea how to write java and make android apps
package com.example.get_flag;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOError;
import java.io.IOException;

import io.michaelrocks.paranoid.Obfuscate;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.CertificatePinner;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

@Obfuscate
public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    private String domain = "downunderctf.com";
    private String scheme = "https://";
    private String port = "443";

    Button button1;
    Button button2;
    Button button3;
    Button button4;
    TextView restext;

    private Handler mHandler;
    private OkHttpClient client;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button1 = (Button) findViewById(R.id.b1);
        button2 = (Button) findViewById(R.id.b2);
        button3 = (Button) findViewById(R.id.b3);
        button4 = (Button) findViewById(R.id.b4);
        restext = (TextView) findViewById(R.id.statusTextView);

        CertificatePinner certificatePinner = new CertificatePinner.Builder()
                .add(domain, "sha256/9BAH1tna31gGCVx9PiXNwZ23wezi9YDGBSiUflTu8dM=")
                .add(domain, "sha256/YLh1dUR9y6Kja30RrAn7JKnbQG/uEtLMkBgFF2Fuihg=")
                .add(domain, "sha256/Vjs8r4z+80wjNcr1YKepWQboSIRi63WsWXhIMN+eWys=")
                .build();
        this.client = new OkHttpClient.Builder()
                .certificatePinner(certificatePinner)
                .build();
        //this.client = new OkHttpClient();

        button1.setOnClickListener(MainActivity.this);
        button2.setOnClickListener(MainActivity.this);
        button3.setOnClickListener(MainActivity.this);
        button4.setOnClickListener(MainActivity.this);
    }

    @Override
    public void onClick(View v) {
        String path = "/";
        int id = v.getId();
        if(id == R.id.b1) {
            path += H.H0();
        } else if(id == R.id.b2) {
            path += H.H1();
        } else if(id == R.id.b3) {
            path += H.H2();
        } else if(id == R.id.b4) {
            path += H.H3();
        }

        restext.setText(R.string.load);

        mHandler = new Handler(Looper.getMainLooper());

        Request r = new Request.Builder()
                .url(scheme + domain + ":" + port + path)
                .build();

        client.newCall(r).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                System.out.println("fail D:");
                mHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        restext.setText("Failed! :C");
                    }
                });
                System.out.println(e);
            }

            @Override
            public void onResponse(Call call, Response response) {
                final int rr = response.code();
                mHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        String s = "Response Code: " + rr;
                        restext.setText(s);
                    }
                });
            }
        });
    }
}
