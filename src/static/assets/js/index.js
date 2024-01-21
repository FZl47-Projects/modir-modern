
const loading = document.querySelector(".loading")
document.querySelector(".test").style.display="none"
loading.style.display="block"
import { getEducation, GetFoodWithUserId, GetStory, foodMaterials } from './api.js'
import {CheckLogin,separate} from './Services.js'

const userid=CheckLogin();



// service worker
if("serviceWorker" in navigator){
    window.addEventListener("load",()=>{
      navigator.serviceWorker.register("../sw.js")
      .then((res)=>console.log(res))
    })
  }
  // -----------------
  let deferredPrompt;
  const addBtn = document.querySelector(".add-button");
  addBtn.style.display = "none";
  console.log("hello");
  window.addEventListener("beforeinstallprompt", (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later.
    deferredPrompt = e;
    // Update UI to notify the user they can add to home screen
    addBtn.style.display = "block";
  
    window.addEventListener("load", (e) => {
      // hide our user interface that shows our A2HS button
      addBtn.style.display = "none";
      // Show the prompt
      deferredPrompt.prompt();
      // Wait for the user to respond to the prompt
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === "accepted") {
          console.log("User accepted the A2HS prompt");
        } else {
          console.log("User dismissed the A2HS prompt");
        }
        deferredPrompt = null;
      });
    });
  });
  
  // -----------------
let educations = await getEducation()
console.log(educations.reverse());

// set informations 
// set video and poster video for education 

let poster = document.querySelector("#poster")
poster.poster = educations[0].poster
console.log(educations);
console.log(educations[0].file);
poster.innerHTML = `<source id="video" src="${educations[0].file}" type="video/mp4">`
// set title education
document.querySelector("#description").innerHTML = educations[0].description

const renderSlider = async () => {
    const story = await GetStory()
    let slide = document.querySelector("#slide-item")
    story.forEach(item => {
        console.log(item);
        const note = `<div class="swiper-slide">
        <div class="story-item">
          <img src="${item.poseter}" alt="">
        </div>
        </div>`
        slide.innerHTML += note
    })
}
await renderSlider()

// backticke food
const renderFood = async () => {
    // fetch food table
    const food = await GetFoodWithUserId(userid)

    // get element 
    const row = document.querySelector("#row")
    row.innerHTML = ""
    //loop for insert item in element 
    let price = 0

    const prices =async (material)=>{
      let end = 0
    material.forEach(item=>{
      
      end += (item.value*item.materialRaw.price)
      
    })
    return end;
    }
    food.forEach(async (item, index) => {
        const material = await foodMaterials(item.id)
        console.log(item);
        // html code for item food

        // let price2 =JSON.parse(item.material)
       
        const FoodCost = await prices(material)
        let rows = `<div class="col-lg-4 col-md-6 px-1 py-2 food-item">
                <img src="${item.image}" alt="" class="imge-food">
                <div class="title-food">
                <div class="name-food">${item.name}</div>
                </div>
                <div class="price">
                <div>قیمت تمام شده</div>
                <div>${separate(Math.round(FoodCost))}</div>
                <span>تومان</span>
                </div>
            </div>`
        // insert code 
        row.innerHTML += rows
    });
    document.querySelector(".test").style.display="block"
loading.style.display="none"
}

await renderFood()


let slider = document.querySelectorAll(".story-item");
let modal_vitrin = document.querySelectorAll(" #modal-story-modirmodern");
let overalyModals = document.querySelectorAll("#modal-story-modirmodern .inner-modal");
let closeModals = document.querySelectorAll(".btn-exit");

slider.forEach((item, index) => {
    item.addEventListener("click", () => {
        console.log(slider);
        console.log(index);
        modal_vitrin[index].classList.add("active");
    });

});
overalyModals.forEach((item, index) => {

    item.addEventListener("click", (e) => {
        if (e.target.className === "inner-modal") {
            modal_vitrin[index].classList.remove("active");
        }
    });
})
closeModals.forEach((item, index) => {
    item.addEventListener("click", () => {
        modal_vitrin[index].classList.remove("active");
    });

});
