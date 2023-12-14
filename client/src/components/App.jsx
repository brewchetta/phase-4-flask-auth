import { useState } from 'react'
import UserPanel from "./UserPanel"
import Notes from "./Notes"

const POST_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

const URL = "http://localhost:5555/api"

function App() {

  // STATE //

  const [currentUser, setCurrentUser] = useState(null)


  // SIGNUP, LOGIN AND LOGOUT FNS //

  // SIGNUP //
  async function attemptSignup(userInfo) {
    const res = await fetch(URL + '/users', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json()
      setCurrentUser(data)
    } else {
      alert('Invalid sign up')
    }
  }

  // LOGIN //
  async function attemptLogin(userInfo) {
    const res = await fetch(URL + '/login', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (res.ok) {
      const data = await res.json()
      setCurrentUser(data)
    } else {
      alert('Invalid sign up')
    }
  }

  // LOGOUT //
  function logout() {
    setCurrentUser(null)
  }


  // RENDER //

  return (
    <div className="App">

      <h1>Authentication + Authorization</h1>

      <UserPanel
      currentUser={currentUser}
      attemptLogin={attemptLogin}
      attemptSignup={attemptSignup}
      logout={logout} />

      <Notes />

    </div>
  );
}

export default App;
