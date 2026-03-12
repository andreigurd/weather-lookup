import os

# List of keys we expect to have set
expected_keys = ['OPENWEATHER_API_KEY']

print("Environment Variable Check")
print("=" * 40)

for key in expected_keys:
    value = os.getenv(key)
    if value:
        # Only show first 8 characters for security
        masked = value[:8] + "..." + value[-4:]
        print(f"  {key}: {masked}")
    else:
        print(f"  {key}: NOT SET!")
        print(f"    -> Set it with: set {key}=your_key_here  (Windows)")
        print(f"    -> Or with:     export {key}=your_key_here  (Mac/Linux)")

print("=" * 40)
