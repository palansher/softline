let tm;//объект для таймера
let cars = [];//массив для картинок
let cx = [];//массив для координат каждой машины
let gameBegin;//переменная используется, чтобы во время движения кнопка Старт была неактивной

let summa = +prompt("Введите вашу сумму");
let c = +prompt("На какую машину (от 0 до 4) вы делаете ставку");
let stavka = +prompt("Сколько вы ставите на выигрыш");
function go()
{
	
	if(summa < stavka){
		alert('У Вас недостаточно средств для начала игры!');
		return;
	}
	
	if (gameBegin==1) return;
	gameBegin = 1;	
	
	for (let i=0; i<5; i++)
	{
	   cars[i] = document.querySelector("#p"+i);
       cars[i].style.border = "none";
       cx[i] = 680;//точка старта
	}
	
	tm = setInterval(timerGo, 50);
   
}

function timerGo()
{
	for (let i=0; i<5; i++)
	{
          //случайный шаг перемещения для автомобиля 
	   cx[i] -= parseInt(Math.random()*7+2);
	   if (cx[i]<=0)
	   {
		  clearInterval(tm);//остановили движение для всех авто
          gameBegin = 0;//разблокировали кнопку Старт
          if(i==c){
              alert("Вы победили");
              summa += stavka;
          }else{
              alert("Вы проиграли. До финиша доехала машина с номером "+i);
			  summa -= stavka;
			  alert("Ваша сумма = "+summa);
          }
          cars[i].style.border = "5px ridge yellow";
          return;
	   }
		cars[i].style.left = cx[i]+"px";	   
	}	
}