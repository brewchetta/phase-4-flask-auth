import { useState, useEffect } from 'react'
import Login from "./Login"
import Signup from "./Signup"
import UserDetails from "./UserDetails"
import Cartoons from "./Cartoons"

function App() {

  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    fetch('/check_session')
    .then(res => {
      if (res.ok) {
        res.json()
        .then( data => setCurrentUser(data) )
      }
    })
  }, [])

  function attemptSignup(userInfo) {
    fetch('/login', {
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
    fetch('/logout', { method: "DELETE" })
  }

  return (
    <div className="App">

      { !currentUser ? <Signup attemptSignup={attemptSignup} /> : null }

      { currentUser ? <UserDetails currentUser={currentUser} logout={logout} /> : null }

      <Cartoons currentUser={currentUser} />

    </div>
  );
}

export default App;
