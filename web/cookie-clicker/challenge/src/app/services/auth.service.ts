import {Injectable} from '@angular/core';
import {User, UserDto} from "../models/user.dto";
import {AngularFireAuth} from "@angular/fire/auth";
import {AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument} from "@angular/fire/firestore";
import {Observable, of} from "rxjs";
import {Router} from "@angular/router";
import {switchMap, take} from "rxjs/operators";
import * as firebase from 'firebase/app';
import DocumentReference = firebase.firestore.DocumentReference;
import {NzMessageService} from "ng-zorro-antd";


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  usersCollection: AngularFirestoreCollection<UserDto>;
  user$: Observable<User>;

  increment = firebase.firestore.FieldValue.increment(1);

  cookie$: Observable<{cookieCount}>;


  constructor(private auth: AngularFireAuth,
              private afs: AngularFirestore,
              private router: Router,
              private message: NzMessageService) {
    this.user$ = this.auth.authState.pipe(
      switchMap(user => {
        if(user) {
          return this.afs.doc<User>(`users/${user.uid}`).valueChanges()
        } else {
          return of(null)
        }
      })
    )

    this.cookie$ = this.afs.doc<{cookieCount}>('cookies/total').valueChanges();
  }

  updateUserData({uid, email}: User) {
    const userRef: AngularFirestoreDocument<User> = this.afs.doc(`users/${uid}`);

    const data = {
      uid,
      email
    };

    return userRef.set(data, {merge: true})
  }

  async registerUser(user: UserDto) {
    const credential = await this.auth.createUserWithEmailAndPassword(user.email, user.password)
    return this.updateUserData(credential.user)

  }

  async login(user: UserDto) {
    // console.log(user)
    const credential = await this.auth.signInWithEmailAndPassword(user.email, user.password)
    return this.updateUserData(credential.user)
  }

  async signOut() {
    await this.auth.signOut();
    this.router.navigate(['login']);
  }

  clickCookie() {
    this.user$.pipe( take(1)).subscribe(data => {
      const batch  = this.afs.firestore.batch()


      const userRef: DocumentReference = this.afs.collection(`users`).doc(data.uid).ref //.update({cookieCount: this.increment})
      const statsRef = this.afs.doc(`cookies/total`).ref

      batch.set(userRef, {cookieCount: this.increment}, {merge: true})
      batch.set(statsRef, {cookieCount: this.increment}, {merge: true})
      batch.commit();
    })
  }


}
