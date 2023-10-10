package com.example.cs370finalproject

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        //when the user presses the grade button go to Signup activity
        findViewById<Button>(R.id.bSignup).setOnClickListener {
            startActivity(Intent(this, SignupActivity::class.java))
        }
        //when the user presses the grade button go to Login activity
        findViewById<Button>(R.id.bLogin).setOnClickListener {
            startActivity(Intent(this, LoginActivity::class.java))
        }
    }
}