import Array "mo:base/Array";

actor {
  type User = {
    name: Text;
    btcBalance: Nat;
    loan: Nat;
  };

  stable var users: [User] = [];

  // Register a new user
  public func registerUser(name: Text): async Text {
    let exists = Array.filter<User>(users, func(u: User): Bool {
      u.name == name
    });
    if (exists.size() > 0) {
      return "User already registered.";
    };

    let newUser: User = {
      name = name;
      btcBalance = 0;
      loan = 0;
    };
    users := Array.append(users, [newUser]);
    return "User registered: " # name;
  };

  // Get all registered users
  public query func getAllUsers(): async [User] {
    return users;
  };

  // Deposit BTC into a user account
  public func deposit(name: Text, amount: Nat): async Text {
    var updated = false;
    users := Array.map<User, User>(users, func(u: User): User {
      if (u.name == name) {
        updated := true;
        { name = u.name; btcBalance = u.btcBalance + amount; loan = u.loan }
      } else {
        u
      }
    });
    if (updated) {
      return "Deposit successful for " # name;
    } else {
      return "User not found.";
    }
  };

  // Request a loan
  public func takeLoan(name: Text, amount: Nat): async Text {
    var updated = false;
    users := Array.map<User, User>(users, func(u: User): User {
      if (u.name == name) {
        updated := true;
        { name = u.name; btcBalance = u.btcBalance; loan = u.loan + amount }
      } else {
        u
      }
    });
    if (updated) {
      return "Loan granted to " # name;
    } else {
      return "User not found.";
    }
  };
};
