"use client"
import React from "react";
const apiUrl = "http://localhost:8000/api/auth";

const ForgotPasswordPage: React.FC = () => {
  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold mb-4">Forgot Password?</h1>
      <p>メールアドレスを入力してください</p>
      <form action={`${apiUrl}/forgot-password`} method="post">
        <input
          type="email"
          name="email"
          placeholder="Email"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
        >
          Reset Password
        </button>
      </form>
    </div>
  );
};

export default ForgotPasswordPage;
