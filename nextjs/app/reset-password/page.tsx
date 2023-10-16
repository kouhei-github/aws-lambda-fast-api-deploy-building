'use client'
import {useEffect, useState} from "react";

const apiUrl = "http://localhost:8000/api/auth";

const RenewPasswordComponent: React.FC = () => {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isValidPasswordResetToken, setIsValidPasswordResetToken] = useState(false);
  const [resetToken, setResetToken] = useState("");

  useEffect(() => {
    // Get the password reset token from the query string.
    const token = new URLSearchParams(window.location.search).get("token");
    if (!token) {
      return;
    }

    // Verify the password reset token.
    async function verifyPasswordResetToken(token: string) {
      const response = await fetch(`${apiUrl}/verify-password-reset-token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          token,
        }),
      });

      // Check the response status code.
      if (response.status !== 200) {
        // The token is invalid.
        // Return an error message to the user
        return "Invalid token. Please try again.";
      }

      // The token is valid.
      // Allow the user to reset their password.
      setIsValidPasswordResetToken(true);
      setResetToken(token);
    }

    verifyPasswordResetToken(token);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
      if (newPassword !== confirmPassword) {
        const message = "Passwords do not match.";
        alert(message);
        return;
      }
      const response = await fetch("/api/auth/renew-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          resetToken,
          newPassword,
        }),
      });

      // Check the response status code.
      if (response.status !== 200) {

        // The token is invalid.
        // redirect to the sign in page
        window.location.href = "/signin";
        return;
      }
  };

  if (!isValidPasswordResetToken) {
    return <div>トークンが不正です、もう一度お試しください</div>;
  }
  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-3xl font-bold mb-4">Renew Password</h1>
      <form action="/api/auth/renew-password" method="post" onSubmit={handleSubmit}>
        <input
          type="password"
          name="newPassword"
          placeholder="New Password"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          className="mb-4 border border-gray-300 rounded-md p-2 w-full"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md"
        >
          パスワードリニューアル
        </button>
      </form>
    </div>
  );
};

export default RenewPasswordComponent;
