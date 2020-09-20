import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router} from "@angular/router";
import {NzMessageService} from "ng-zorro-antd";
import {UserDto} from "../models/user.dto";
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  validateForm: FormGroup;
  loading = false;

  constructor(private fb: FormBuilder,
              private router: Router,
              private authService: AuthService,
              public messageSvc: NzMessageService) {}

  submitForm(): void {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }

    if (this.validateForm.valid) {
      console.log(this.validateForm.value);
      const user: UserDto = this.validateForm.value;

      this.loading = true;
      const logginginmsg = this.messageSvc.loading("Creating your account...").messageId

      this.authService.registerUser(user)
        .then(data => {
          this.messageSvc.success("Successfully registered")
          this.router.navigate([''])
        })
        .catch( (error) => {
          // Handle Errors here.
          var errorCode = error.code;
          var errorMessage = error.message;
          if (errorCode == 'auth/weak-password') {
            this.messageSvc.error('The password is too weak.');
          } else {
            this.messageSvc.error(errorMessage);
          }
        }).finally(() => {
          this.messageSvc.remove(logginginmsg);
          this.loading = false;
      })
    }
  }



  ngOnInit(): void {
    // this.authService.logout();

    this.validateForm = this.fb.group({
      email: [null, [Validators.required, Validators.email]],
      password: [null, [Validators.required]],
    });
  }

}
