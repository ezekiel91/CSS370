package com.example.cs370finalproject

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import com.google.firebase.firestore.FirebaseFirestore

class SignupActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_signup)

        //when the user presses the grade button go to grade activity
        findViewById<Button>(R.id.bBack).setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }


        findViewById<Button>(R.id.bCreateaccount).setOnClickListener {
            val fullName = findViewById<EditText>(R.id.Name).text.toString()
            val email = findViewById<EditText>(R.id.Email).text.toString()
            val password = findViewById<EditText>(R.id.Password).text.toString()
            val confirmPassword = findViewById<EditText>(R.id.Confirm).text.toString()
            val db = FirebaseFirestore.getInstance()
            val account: MutableMap<String, Any> = HashMap()
            account["fullName"] = fullName
            account["email"] = email
            account["password"] = password
            account["confirmPassword"] = confirmPassword
            db.collection("account")
                .add(account)
                .addOnSuccessListener {
                    Log.d("dbfirebase", "save: ${account}")
                }
                .addOnFailureListener {
                    Log.d("dbfirebase Failed", "${account}")
                }
            db.collection("account")
                .get()
                .addOnCompleteListener {
                    val result: StringBuffer = StringBuffer()
                    if (it.isSuccessful) {
                        val text = "Account created"
                        val duration = Toast.LENGTH_SHORT
                        val toast = Toast.makeText(this, text, duration)
                        toast.show()
                        for (document in it.result!!) {
                            Log.d("dbfirebase", "retrieve: " +
                                    "${document.data.getValue("fullName")}" +
                                    "${document.data.getValue("email")}" +
                                    "${document.data.getValue("password")}" +
                                    "${document.data.getValue("confirmPassword")}")
                        }
                    }
                }
        }
    }
}