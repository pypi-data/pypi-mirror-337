import React, { useState } from 'react'
export default function Q1() {
    const [value,setvalue]=useState('')
    const handlesubmit=(f)=>{
      f.preventDefault()
      console.log(`form submited with input value ${value}`)
    }
    const inputhandle=(e)=>{
        setvalue(e.target.value)
    }
  return (
    <div>
    <form onSubmit={handlesubmit}>
      <h1>Value :{value}</h1>
        <input type='text' onChange={inputhandle} />
        <button type='submit'>Submit</button>
    </form>
    </div>
  )
}
