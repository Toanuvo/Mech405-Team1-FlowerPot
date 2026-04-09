from Flowerpot_Engine import *
def main():
    r
    print("Hello from mech405-team1-flowerpot!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('\nBye...')
