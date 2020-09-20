import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {AngularFireModule} from "@angular/fire";
import {environment} from "../environments/environment";
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import {
  NgZorroAntdModule,
  NzBreadCrumbModule,
  NzButtonModule,
  NzFormModule, NzIconModule, NzInputModule,
  NzLayoutModule, NzMenuModule,
  NzMessageModule
} from "ng-zorro-antd";
import {AngularFireAuthModule} from "@angular/fire/auth";

registerLocaleData(en);

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularFireModule.initializeApp(environment.firebase),
    // AngularFireAuthModule,
    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    NzButtonModule,
    NzMessageModule,
    NzBreadCrumbModule,
    NzFormModule,
    NzLayoutModule,
    NzInputModule,
    NzMenuModule,
    NzIconModule,
    BrowserAnimationsModule,
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US }],
  bootstrap: [AppComponent]
})
export class AppModule { }
