import React, { useState } from "react";

import "./Register.css";


const Register = () => {
  const [userName, setUserName] =
    useState("");

  const [firstName, setFirstName] =
    useState("");

  const [lastName, setLastName] =
    useState("");

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");


  const register = async (event) => {
    event.preventDefault();

    const response = await fetch(
      "/djangoapp/register",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json",
        },

        body: JSON.stringify({
          userName,
          firstName,
          lastName,
          email,
          password,
        }),
      }
    );


    const data =
      await response.json();


    if (
      data.status ===
      "Authenticated"
    ) {
      sessionStorage.setItem(
        "username",
        data.userName
      );

      sessionStorage.setItem(
        "firstname",
        data.firstName
      );

      sessionStorage.setItem(
        "lastname",
        data.lastName
      );

      window.location.href = "/";
      return;
    }


    if (
      data.error ===
      "Already Registered"
    ) {
      alert(
        "Username already registered."
      );

      return;
    }


    alert(
      "Registration failed."
    );
  };


  return (
    <div className="register_container">

      <h1>Sign Up</h1>

      <form onSubmit={register}>

        <div className="input">
          <label>Username</label>

          <input
            type="text"
            placeholder="Username"
            required
            onChange={(event) =>
              setUserName(
                event.target.value
              )
            }
          />
        </div>


        <div className="input">
          <label>First Name</label>

          <input
            type="text"
            placeholder="First Name"
            required
            onChange={(event) =>
              setFirstName(
                event.target.value
              )
            }
          />
        </div>


        <div className="input">
          <label>Last Name</label>

          <input
            type="text"
            placeholder="Last Name"
            required
            onChange={(event) =>
              setLastName(
                event.target.value
              )
            }
          />
        </div>


        <div className="input">
          <label>Email</label>

          <input
            type="email"
            placeholder="Email"
            required
            onChange={(event) =>
              setEmail(
                event.target.value
              )
            }
          />
        </div>


        <div className="input">
          <label>Password</label>

          <input
            type="password"
            placeholder="Password"
            required
            onChange={(event) =>
              setPassword(
                event.target.value
              )
            }
          />
        </div>


        <button
          type="submit"
          className="submit"
        >
          Register
        </button>

      </form>

      <p>
        Already registered?{" "}

        <a href="/login">
          Login
        </a>
      </p>

    </div>
  );
};


export default Register;