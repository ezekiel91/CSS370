package com.example.cs370finalproject

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.firestore.FirebaseFirestore

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        //when the user presses the grade button go to Login activity
        findViewById<Button>(R.id.bBack2).setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }

        findViewById<Button>(R.id.bLogin2).setOnClickListener {
            var success = false
            val email = findViewById<EditText>(R.id.email2).text.toString()
            val password = findViewById<EditText>(R.id.password2).text.toString()
            val db = FirebaseFirestore.getInstance()
            val account: MutableMap<String, Any> = HashMap()
            account["email"] = email
            account["password"] = password
            db.collection("account")
                .get()
                .addOnCompleteListener {
                    if (it.isSuccessful) {
                        for (document in it.result!!) {
                            if ((document.data.getValue("email") == email) && (document.data.getValue("password") == password)) {
                                success = true
                                startActivity(Intent(this, VideoActivity::class.java))
                            }

                        }
                    }
                    if (!success) {
                        val text = "Either ID or password is incorrect"
                        val duration = Toast.LENGTH_SHORT

                        val toast = Toast.makeText(this, text, duration) // in Activity
                        toast.show()
                    }
                }
        }
    }
}
