import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpClientJsonpModule} from "@angular/common/http";

declare var $: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'app';
  src:string;
  vsrc:string;

  constructor(private http: HttpClient){}

  ngOnInit(){


    // var img:HTMLImageElement = new Image();
    this.src = "/assets/diagram.jpg";
    this.vsrc = "http://dev.omnifit.co.kr/mnt/wait/download/WT1000000061/ces_mv.mp4";
    // this.src = "https://api.cryptowat.ch/pairs/btcusd";


    // function draw(img: HTMLImageElement) {
    //
    // }
    //
    // img.onload = function() {
    //   draw(img);
    // };

    // var img = document.querySelector('#img');


    // console.log("-------"+img);
    // this.http.get("https://api.cryptowat.ch/pairs/btcusd").subscribe(it=>console.log(it));
    // let g = this.http.jsonp("https://api.cryptowat.ch/pairs/btcusd",'gg').subscribe(it=>console.log(it));
    // console.log("-------",g);

  }

  vonload(event){
    console.log("video-->",event.srcElement);
  }

  onload(event){
    // console.log(event);
    // var img:HTMLImageElement = event.srcElement;
    // var canvas:HTMLCanvasElement = document.querySelector('#can') as HTMLCanvasElement;
    // // this._canvas = <HTMLCanvasElement> yourHtmlElement;
    // // this._canvas = yourHtmlElement as HTMLCanvasElement;
    //
    // var context = canvas.getContext('2d');
    // context.drawImage(img, 0, 0);
    // var imageData:ImageData = context.getImageData(100, 100, 100, 100);
    // console.log("img data",imageData);
  }

}
