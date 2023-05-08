import { useState, useEffect } from 'react'
import Login from "./Login"
import Signup from "./Signup"
import UserDetails from "./UserDetails"
import Cartoons from "./Cartoons"

function App() {

  const [currentUser, setCurrentUser] = useState(null)

  function attemptSignup(userInfo) {
    fetch('/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accepts': 'application/json'
      },
      body: JSON.stringify(userInfo)
    })
    .then(res => res.json())
    .then(data => setCurrentUser(data))
  }

  function logout() {
    setCurrentUser(null)
  }

  return (
    <div className="App">

      <Signup attemptSignup={attemptSignup} />

      { currentUser ? <UserDetails currentUser={currentUser} logout={logout} /> : null }

      <Cartoons />

    </div>
  );
}

export default App;
