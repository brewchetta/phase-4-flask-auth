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

  function attemptLogin(userInfo) {
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accepts': 'application/json'
      },
      body: JSON.stringify(userInfo)
    })
    .then( res => {
      if (res.ok) {
        res.json()
        .then( data => setCurrentUser(data) )
      } else {
        res.json()
        .then( data => alert(data.message) )
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
    .then(res => res.json())
    .then(data => setCurrentUser(data))
  }

  function logout() {
    setCurrentUser(null)
    fetch('/logout', {
      method: 'DELETE'
    })
  }

  return (
    <div className="App">

      <Signup attemptSignup={attemptSignup} />
      <Login attemptLogin={attemptLogin} />

      { currentUser ? <UserDetails currentUser={currentUser} logout={logout} /> : null }

      <Cartoons />

    </div>
  );
}

export default App;
