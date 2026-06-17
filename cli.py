import argparse
from weather.agent import run_weather_agent
from weather.high_lows import daily_high_low_now
from weather.fetch import get_current_conditions

def main():
    parser = argparse.ArgumentParser(
        description="Bonsai Weather Agent CLI"
    )

    parser.add_argument(
        "command",
        choices=["weather", "highs", "wind"],
        help="Choose what to check"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print raw weather data"
    )

    args = parser.parse_args()

    if args.command == "weather":
        if args.debug:
            print("Running in debug mode...")
        run_weather_agent()

    elif args.command == "highs":
        hl = daily_high_low_now(35.0456, -85.3097)
        print(f"Today's High: {hl['high_f']}°F")
        print(f"Today's Low:  {hl['low_f']}°F")

    elif args.command == "wind":
        cond = get_current_conditions()
        print(f"Wind Speed: {cond['wind_mph']} mph")

if __name__ == "__main__":
    main()
