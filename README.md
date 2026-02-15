# hypermedia-webapp
Working through https://hypermedia.systems/a-web-1-0-application/

## APIs

This project includes three hypermedia interfaces:

1. **HTML/HTMX** - Web browser interface (routes: `/contacts`)
2. **JSON** - REST API (routes: `/api/v1/contacts`)
3. **HXML** - Hyperview mobile interface (routes: `/hv/contacts`)

## Installing/Updating js dependencies

```shell
HTMX_VERSION=2.0.8 # This should match the value in layout.html
curl https://cdn.jsdelivr.net/npm/htmx.org@${HTMX_VERSION}/dist/htmx.js -o src/static/js/htmx.${HTMX_VERSION}.js
```

## Run

Run using uv:

```shell
uv run server
```

or, to have changes trigger a reload:

```shell
uv run dev-server
```

## Testing the Hyperview Mobile UI

The HXML API provides a native mobile interface using [Hyperview](https://hyperview.org/). The endpoints are available at `/hv/contacts`.

### Quick Start: Testing with curl

You can view the HXML responses directly:

```shell
# Start the dev server
uv run dev-server

# In another terminal, test the HXML endpoints
curl http://localhost:5000/hv/contacts
curl http://localhost:5000/hv/contacts/1
```

### Testing with a Real Mobile App

To test the Hyperview UI in an actual mobile app, you have several options:

> **Note:** The Hyperview demo app's entry point is configured in `demo/App.tsx`. By default, it points to `${baseUrl}/hyperview/public/index.xml`. To test with your contacts app:
> 1. Edit `demo/App.tsx`
> 2. Change the `entrypointUrl` prop from:
>    ```typescript
>    entrypointUrl={`${Constants.expoConfig?.extra?.baseUrl}/hyperview/public/index.xml`}
>    ```
>    to:
>    ```typescript
>    entrypointUrl={`${Constants.expoConfig?.extra?.baseUrl}/hv/contacts`}
>    ```
> 3. Set `BASE_URL` environment variable when starting to point to your Flask server

#### Option 1: Use Expo Go on a Physical Device (Easiest)

1. **Install Expo Go** on your iOS or Android device from the app store
   - [iOS App Store](https://itunes.apple.com/us/app/expo-client/id982107779?mt=8)
   - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. **Clone and set up the Hyperview demo app:**
   ```shell
   git clone https://github.com/Instawork/hyperview.git
   cd hyperview/demo
   yarn install
   ```

3. **Start the demo backend server:**
   ```shell
   yarn server
   ```
   This will start a server on port 8085 serving the demo HXML files.

4. **In a separate terminal, start the Expo development server:**
   ```shell
   # Replace X.X.X.X with your machine's IP address
   # Find it with: ip addr show (Linux) or ifconfig (macOS)
   BASE_URL="http://X.X.X.X:8085" yarn start
   ```

   For PowerShell:
   ```powershell
   $env:BASE_URL="http://X.X.X.X:8085"; yarn start
   ```

   For testing with your contacts app, use `BASE_URL="http://X.X.X.X:5000"` (bash/Linux) or `$env:BASE_URL="http://X.X.X.X:5000"; yarn start` (PowerShell) - see note above about editing `App.tsx`

5. **Scan the QR code** with your phone's camera (iOS) or Expo Go app (Android)

#### Option 2: Android Emulator (Linux/Windows/macOS)

1. **Install Android Studio** and set up an Android Virtual Device (AVD)

2. **Clone and set up the Hyperview demo app:**
   ```shell
   git clone https://github.com/Instawork/hyperview.git
   cd hyperview/demo
   yarn install
   ```

3. **Start the demo backend server:**
   ```shell
   yarn server
   ```

4. **In a separate terminal, configure port forwarding and run the app:**
   ```shell
   adb reverse tcp:8085 tcp:8085
   yarn android
   ```

   For testing with your contacts app: `adb reverse tcp:5000 tcp:5000` and see note above about editing `App.tsx`

#### Option 3: iOS Simulator (macOS only)

1. **Install Xcode** from the App Store

2. **Clone and set up the Hyperview demo app:**
   ```shell
   git clone https://github.com/Instawork/hyperview.git
   cd hyperview/demo
   yarn install
   ```

3. **Start the demo backend server:**
   ```shell
   yarn server
   ```

4. **In a separate terminal, run the app:**
   ```shell
   yarn ios
   ```

   For testing with your contacts app, edit `demo/app.config.ts` to set `baseUrl: 'http://localhost:5000'` and see note above about editing `App.tsx`

### HXML Endpoints Available

- `GET /hv/contacts` - List all contacts with search
- `GET /hv/contacts/<id>` - View contact details
- `GET /hv/contacts/new` - New contact form
- `POST /hv/contacts/new` - Create new contact
- `GET /hv/contacts/<id>/edit` - Edit contact form
- `POST /hv/contacts/<id>/edit` - Update contact
- `DELETE /hv/contacts/<id>` - Delete contact
- `GET /hv/contacts/<id>/email/validate` - Validate email field
- `GET /hv/contacts/count` - Get total count

### Debugging Tips

- Use your browser to view HXML responses: `http://localhost:5000/hv/contacts`
- Check the Flask console for errors when the mobile app makes requests
- Ensure your phone/emulator and computer are on the same network
- Disable firewall on port 5000 if the mobile app can't connect

## Original full version

See [https://github.com/bigskysoftware/contact-app](https://github.com/bigskysoftware/contact-app)
