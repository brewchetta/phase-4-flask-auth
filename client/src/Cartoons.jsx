import { useState, useEffect } from 'react'

function Cartoons() {

  const [cartoons, setCartoons] = useState([])

  useEffect(() => {
    fetch('/cartoons')
    .then(res => {
      if (res.ok) {
        res.json()
        .then(data => setCartoons(data))
      }
    })
  }, [])

  return (

    <div>

      { cartoons.map(cartoon => <h3>{cartoon.id} {cartoon.name}</h3>) }

    </div>

  )

}

export default Cartoons
