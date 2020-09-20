import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {NzMessageService} from "ng-zorro-antd";
import {UserDto} from "../models/user.dto";
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  validateForm: FormGroup;
  loading = false;

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }

    if (this.validateForm.valid) {
      console.log(this.validateForm.value);
      const user: UserDto = this.validateForm.value;

      this.loading = true;
      const logginginmsg = this.message.loading("Logging in...").messageId

      this.authService.login(user)
        .then(data => {
          this.message.success("Logged in!")
          this.router.navigate([''])
        })
        .catch((error) => {
          // Handle Errors here.
          var errorCode = error.code;
          var errorMessage = error.message;
          if (errorCode === 'auth/wrong-password') {
            this.message.error('Wrong password.');
          } else {
            this.message.error(errorMessage);
          }
          console.log(error);
        }).finally(() => {
        this.message.remove(logginginmsg);
        return this.loading = false;

      });
    }
  }

  constructor(private fb: FormBuilder,
              private router: Router,
              private authService: AuthService,
              private message: NzMessageService) {}

  ngOnInit(): void {
    // this.authService.logout();

    this.validateForm = this.fb.group({
      email: [null, [Validators.required]],
      password: [null, [Validators.required]],
    });
  }

}
