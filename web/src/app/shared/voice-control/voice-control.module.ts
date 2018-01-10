import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {ModalModule} from "ngx-bootstrap";

import {SoundModule} from "../sound/sound.module";
import {UtilsModule} from "../utils/utils.module";

import {VoiceControlService} from "./voice-control.service";
import {SpeechButtonComponent} from './speech-button/speech-button.component';
import {VoiceRecognitionService} from "./voice-recognition.service";
import { PopoverModule } from 'ngx-popover';


@NgModule({
  imports: [
    CommonModule, ModalModule, PopoverModule, SoundModule, UtilsModule
  ],
  exports: [
    SpeechButtonComponent,
  ],
  declarations: [
    SpeechButtonComponent,    
  ],
  providers: [VoiceControlService, VoiceRecognitionService],

})
export class VoiceControlModule {
  static forRoot() {
    return {
      ngModule: VoiceControlModule,
      providers: [VoiceControlService, VoiceRecognitionService]
    }
  }
}
