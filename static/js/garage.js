// handels all the slidebar into the garage section 
    const theSection = document.getElementById('bar')
    const closeSection = document.getElementById('close')
    const navberSection = document.getElementById('navber')
  
    if(theSection){
      theSection.addEventListener( 'click',()=>{
          navberSection.classList.add('active')
      })
    }
    if(closeSection){
      closeSection.addEventListener('click',()=>{
          navberSection.classList.remove('active')
      })
    }
