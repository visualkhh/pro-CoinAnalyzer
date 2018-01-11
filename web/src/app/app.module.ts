import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import { HttpClient, HttpClientModule, HttpClientJsonpModule } from '@angular/common/http';
import {AppService} from "./app.service";


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    HttpClientJsonpModule
  ],
  providers: [AppService],
  bootstrap: [AppComponent]
})
export class AppModule { }
