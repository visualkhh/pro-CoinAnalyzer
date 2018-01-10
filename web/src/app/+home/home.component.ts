import { Component, OnInit ,ViewChild, ElementRef, AfterViewInit} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {JsonpModule, Response} from '@angular/http';
import {RequestOptions} from "http";
import {DomSanitizer} from "@angular/platform-browser";
declare var $:any;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public url: any;
  public callback: any;

    constructor(private http: HttpClient,private sanitizer:DomSanitizer) { }

  ngOnInit() {
      this.url = this.sanitizer.bypassSecurityTrustResourceUrl('https://api.cryptowat.ch');
      console.log(this.url);
      this.http.jsonp("https://api.cryptowat.ch/",'callback').subscribe(data=>console.log(data) );
      //
      // let apiURL = `${this.url}`;
      // return this.jsonp.request(apiURL)
      //     .map(res => {
      //         return res.json();
      //     });


    //   let headers = new HttpHeaders();
    //   headers.set('Content-Type','application/json');
    //   headers.set('Accept', 'application/json');
    //   headers.set('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT');
    //   headers.set('Access-Control-Allow-Origin', '*');
    //   headers.set('Access-Control-Allow-Headers', "X-Requested-With, Content-Type, Origin, Authorization, Accept, Client-Security-Token, Accept-Encoding");
    //
    // // this.http.get("https://api.cryptowat.ch/",{headers : headers})
    // this.http.get("https://api.cryptowat.ch/")
    //     .subscribe(res=>console.log(res));
  }

    // onLoad(e) {
    // //asdasd
    //     let body = $(e.srcElement).contents().find('body').html();
    //     console.log(body);
    // }
}
