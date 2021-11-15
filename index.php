<?php
    date_default_timezone_set('Europe/Amsterdam');
    $isThursday = date("w", time()) == 4;
    $message = $isThursday ? "Ja!" : "Nee.";
?><!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Is Het Al Donderdag?</title>
    <meta name="description" content="Wil je weten of het al donderdag is?">
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@700&display=swap&text=JaNe.!?Ishtlondrg" rel="stylesheet" />
    <style>
        :root {
            --font-family: 'Open Sans', sans-serif;
            --text-color: #474747;
            --text-color-active: #0f874b;
            --text-color-inactive: #ec0000;
            --text-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
            --background-color: #fff;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #fff;
                --text-color-active: #14ba67;
                --text-color-inactive: #ec0000;
                --text-shadow: 0 2px 5px rgba(255, 255, 255, 0.5);
                --background-color: #000;
            }
        }
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100vh;
            font-size: 16px;
            background-color: var(--background-color);
        }
        nav { display: none; }
        main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
        }
        h1 {
            margin: 0;
            color: var(--text-color);
            font-family: var(--font-family);
            text-align: center;
        }
        h2 {
            margin: 0;
            font-family: var(--font-family);
            font-size: 4em;
            color: var(--text-color);
            text-shadow: var(--text-shadow);
        }
        .active {
            color: var(--text-color-active);
        }
        .inactive {
            color: var(--text-color-inactive);
        }
    </style>
    <script src="/static/js/main.js" async></script>
</head>
<body>
    <main>
        <h1>Is het al donderdag?</h1>
        <h2 class="<?php echo ($isThursday ? 'active' : 'inactive'); ?>"><?php echo $message; ?></h2>
    </main>
</body>
</html>
