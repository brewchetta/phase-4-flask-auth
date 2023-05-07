import { useState, useEffect } from 'react'
import Login from "./Login"
import Signup from "./Signup"
import UserDetails from "./UserDetails"
import Cartoons from "./Cartoons"

function App() {

  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    fetch('/current_session')
    .then(res => {
      if (res.ok) {
        res.json()
        .then(user => setCurrentUser(user))
      }
    })
  }, [])

  function attemptLogin(userInfo) {
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accepts': 'application/json'
      },
      body: JSON.stringify(userInfo)
    })
    .then(res => {
      if (res.ok) {
        res.json()
        .then(user => setCurrentUser(user))
      }
    })
  }

  function attemptSignup(userInfo) {
    fetch('/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accepts': 'application/json'
      },
      body: JSON.stringify(userInfo)
    })
    .then(res => {
      if (res.ok) {
        res.json()
        .then(user => setCurrentUser(user))
      }
    })
  }

  function logout() {
    setCurrentUser(null)
    fetch('/logout', { method: 'DELETE' })
  }

  return (
    <div className="App">

      { !currentUser ? <Login attemptLogin={attemptLogin} /> : null }

      { !currentUser ? <Signup attemptSignup={attemptSignup} /> : null }

      { currentUser ? <UserDetails currentUser={currentUser} logout={logout} /> : null }

      <Cartoons />
    </div>
  );
}

export default App;
