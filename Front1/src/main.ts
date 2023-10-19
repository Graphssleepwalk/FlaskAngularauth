import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

// fake backend


import { AppComponent } from '@app/app.component';
import { jwtInterceptor, errorInterceptor } from '@app/_helpers';
import { APP_ROUTES } from '@app/app.routes';

bootstrapApplication(AppComponent, {
    providers: [
        provideRouter(APP_ROUTES),
        provideHttpClient(
            withInterceptors([
                jwtInterceptor, 
                errorInterceptor,

            ])
        )
    ]
});
