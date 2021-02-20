# ECE_Team9_Capstone
**AI teaching assistant.  Facial recognition and behavioral processing.**

Elevaor Pitch:
Our sponsor, Christof Teuscher is an Alan Turing enthusiast and avid runner.  His proposal, “An AI-based Teaching Practices and Classroom Activities Tool to Improve Education” is an automated tool that must use AI to analyze student and teaching behaviors using a simple recording device, like a cell phone.  That analysis should include student interaction and presented teaching materials.  It may also consider the teacher's presentation style.  We must deliver a functional prototype using a cell phone to record and analyze full-length class sessions.  We also must deliver relevant documentation.  We expect to encounter COVID related collaboration issues and we are concerned about accidental feature creeping technological overreach.

This project will allow a user, such as a professor, to record their lecture and their student’s response to different moments within that lecture.  These recordings will be uploaded and processed. The user will receive a report back from this program that describes to them how their students responded to different moments throughout that lecture (description detailed in “Requirements”).  The user can then use this feedback to modify their future teaching behaviors to maximize student interaction or student attentiveness in accordance with their goals and repeat the analysis.

Our project must have the ability to receive and analyze one full-length class lecture recording from two perspectives.  These perspectives must include the professor with their presented materials and the student audience.  These recordings will be processed by a program that must be able to analyze those two recordings and produce a visualization, containing information outlined below, in a form where a non-technical user can glean informative feedback.  This feedback will describe the user’s teaching behavior across time and the commensurate effects of those changes on the student audience.

![Block Diagram](https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=Team9_Block%20Diagram.drawio#R7V1bV7JKGP41XvotOeOlh7Qsza2p6U0LYRQSGeSQh1%2B%2FB0EFHEkNFMtqtZhhGGTeh%2Bc9ghmqNF1UDUGX61ACaobMSYsMVc6QJEGTZMb5y0lLt4djvY6xoUjeoF1HW1kBrzPn9dqKBMzAQAtC1VL0YKcINQ2IVqBPMAw4Dw4bQTV4Vl0Yg72Otiio%2B709RbJkt5dncrv%2BR6CM5c2ZiZy3ZypsBnsdpixIcO7roh4yVMmA0HK3posSUJ3F26zLy6Q2Xcw%2Bnt%2BL9JexaDRpmhaz7mSVUw7ZXoIBNOvsqW3qvyKvKS2yMcuprUlvVqyzWU%2BWX4Jqe%2BvlXau13CygAW1NAs4kuQxVnMuKBdq6IDp75wgyqE%2B2pipqEWhzpKhqCarQWB9LjRjnF%2FWblgEnwLeHXf84R0DN8vW7P6j%2FyGv21uYLGBZY%2BCTurUEVwCmwjCUa4u3dCN6DM%2B815ztscLTXJ%2FtwwW46BQ%2BP4%2B3MuzVHG96y40VQe%2B13Fx0we%2BrL2jRnrrhJpelJLSgCVkWnLQ7RxtjZ6KJbCKKGMHWWWxua%2BnqB3FHopNuBe0eWjhqlCqapjBRgHDU6%2FEHgCH38pgFHwDThgSlixJQkAH4kYjEl8mA4ShA7fBA7W47zgYcgceCJATvKS16kJz0DdKvG8tN%2Bl6xJ4RjsFGxJ%2BaXYIW4JO1cFT0tbyhWjX27K%2BadBs0oNVjJ3AvHkTofC6XBbQ6Ft2RJaeDN5FmEAL9E4JPDkkFprpqSQQHNXREKhaGXVsiQ%2FjMmGWe8OOK4u%2FxIaORM7Z7DI9bDDMlfEzpIvPXcelRL1UHygNGk%2BM5tHYWfT4Zh6ASmwMxtudmTNtetQQAMIWl%2Fsdoa4qOIhEZ2XInyidicPnjASAejakA8CbkmHECEdQhwrfT4p6RNXkv4JYk%2Fk4%2BwzIUVeBYzXoyKGTRsYj3BmgSYVnKACaolrlSMGlxcsFOvdMSj%2BMV6r7%2Bz5l9s0ywvP3Fg3lr5GExgKug5gbPo0dE2%2BuZxm379vN9W6tZnrNHmZ0DZEELEolDvOEowxsL7ncSAFwin70vdJl8EId9NnAFWwlK9gEAYnce8MTais70cPXBQZAhcZAo173d5R%2FqhHeKJ8cCImNI%2B7LnvzrPG3verzIUl9z49Pmm5b%2B%2FrsMFeg%2B9MKolZQlbHmQBpBxsFf0bmLFVFQC96OqSJJzuFFAyBmE4brqRyw6c6Fr5eCKWaYsjOXbUGX%2FdZTJ8UeW8PFkwu1Tx4sBl5hGMTGHfRJgiL%2FjqCYfLoExcRK8gQXoHnidJqPma7pI%2BmaSBVd07kQSMLuxrF0TYf8G4q4LF%2BzB2ngaHsxh7MXW0CEhqRoY2dyz5QV%2FKbs0DhkWo4MOHUQhgmSBc3M38g%2BJB3EAyZcj7UxqaToh0stQMz98MfvxwdLpgwffIzqya%2BaovVSOlyN3L7uisp4pVV3hTN95%2BouMn9Z3bVRlXFgj%2FgF2IvKmN2xFzP2cIHAv8J7m7IWH%2FaiEm537MWMvRjjfjfHexjsRaX47tiLGXuHA3w%2F8wc2mfeRgo7%2BSxY9EY78brLl1wo4EYdDg3cRnxdSJNImYlxQMQ4Rb3LVf07EZD5tIj4c2TN1QYtdxO6kv1nELHc9Edeyq9FyuCBaH0Kr8ap21PZgFVGJcvRNzB7I9QcTQW0VMTcaXtAEdbmKLln67m43ZUF3NpF8BFUFKhwbwtQRqy%2FNENjnyz98XyuwAJuKfFxx9mhEithCFokdskyStQNESANs7UF%2F3A5Xhh1H7cAbP4Yl%2BMiIS%2BMZvg7m5kRrXBA8OhAmbpy36QjuF8AIsAdgxOWHudN9nuNhRFFXhFFhwozbKv0lZmvd6n%2BtTqNsZi8HoydHTwiipUDtF0CIFwEeQkOecVy8BG1R5ooQEiVTHU5WzCPs1j9HdeFD7hFYCJ0bSftHBsqYUhbQiEoOBJIIEdo%2BpQGNPXicHdAIZ6riC2hUACwVQLH0VSV6xJdlNuYLMYLAfmYmb2wmzZ4OHZ7KCZqUcUzBcHZzbRsjsUHD2S9CW3Nrbiro%2Fxvim1Ta2Aa0hDUVU2WWTJCtQib3tkrOT1YEBuVxpDub71K3Uv%2FojFaC2jUVmJU7r%2FGSFXcWWZEpY6so8zKlbLV9IuWnbEWHnbv42AoLv8Pl54mw1a1zU6IP1hJsmJyYfXLKY0AdR0CAerK14WdXYR6L1VqhOnuoP8N4ySnNhlRUpvtOTYlT0xSwT51BvdGXpBqffV5YBdBKzJDqueSju7GD2%2BEelkk0EMB8axglRT0V0NE%2B8%2B9vr%2B2mtci2m1Sj3kuDE3cpuyiq1CGQlo6Il9zJ5wdeHAZ%2BidlFbo2pcyGWhTbQUmvANG%2BKiBguQSKi94ygI8NJcTCRxemVR7jI9kugPJq03j7k2UsaPLQ7Ef0FIsKiL3kikl3XzNZvioQStYYY%2BggSwlXFx0FC%2FWktO9B7ucfx%2BEUzO%2F2KQY2v7okRl2GgqMq7G2MgJvSqAeoGGAgUy%2FKiZjMdfjhoVcck5N%2FJCzDQfgx7ZgPTudFvwDBKioO4cIUn5u0AOI8sjkh1qbCcv65Gwiwrd9gXlaosJrUYMrMkcVRmtquYNhLYD7OxR78QQjB197WJ6xxrZi%2B3CgiJAY7Ju5dbzbMcJSRZ5RH2yhlMhRBBYUBAxIGCjqS%2Fl4zaeDBQuOd3tTTqdT9iVURnmMIBNbSzi%2BPPVURkTP2KKOpOSYkiCpvCTPiJ4LMVUfgZ5fgUERZ6SSmiArohnXegogm8rIUbG0yhsvGnIpI0gMOpiG2Rh594cgkZwCU4t62C2Z92iPrrm%2FJVpHvx8s4pXvidQm6UQrAoSopC3tB9qfoIxMtspptB6CTLwpCog5C5YEJBHY%2BePhY6JRrzoVa1HwTTnl7dg75YFC8qR3nnncR5Bwu%2BpHjHy2WaOnJMtK2v7LFQCtknKbbZBwqmdCIpe6VqWvZDlR68tlcfZeuFflw%2B21fLX57PG1ExtRvnDTYXE29s7eD4eQOLosTtlW0MzhdxSyFv%2BKyWbKJmSzj9uM0EXCLyT8tfBQlAgfvUJ3Wr9EE15viHsi7h%2BBwI%2FScYc7kT0FUJCIu%2B5IP%2F%2FlC%2FIBrQKYY4%2BJL0ICPF8UHMUKFqysmPyidJfvwBsF2iABX77TpXctrO57Ab4Ka9F%2FqGKeVobgqRHJccN2HBccSr09dfyXXc9xn8Cj%2BI4g6I5AKPlGNlhHv1x6k38C6CkqP4oDFCUdsRB8yRdetnr5y9MduDYLkABuizn6QLVcEkGDTBYiepV8me9GzKxiTJWcEChPS8gcSfE%2BIT5BYiBAeca0TG5Bqh5u5rAV087b5ckXr4Hw%3D%3D)

[Proposal Document](https://docs.google.com/document/d/1YcNP2XVLgDVtbruc-ptutkXsHnPfJws35ECDuVT-Fk0/edit?usp=sharing)
