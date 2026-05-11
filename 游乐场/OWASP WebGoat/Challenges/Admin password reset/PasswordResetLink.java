/*    */ import java.util.Random;
/*    */ 
/*    */ public class PasswordResetLink {
/*    */   public String createPasswordReset(String paramString1, String paramString2) {
/* 14 */     Random random = new Random();
/* 15 */     if (paramString1.equalsIgnoreCase("admin"))
/* 17 */       random.setSeed(paramString2.length()); 
/* 19 */     return scramble(random, scramble(random, scramble(random, MD5.getHashString(paramString1))));
/*    */   }
/*    */   
/*    */   public static String scramble(Random paramRandom, String paramString) {
/* 23 */     char[] arrayOfChar = paramString.toCharArray();
/* 24 */     for (byte b = 0; b < arrayOfChar.length; b++) {
/* 25 */       int i = paramRandom.nextInt(arrayOfChar.length);
/* 26 */       char c = arrayOfChar[b];
/* 27 */       arrayOfChar[b] = arrayOfChar[i];
/* 28 */       arrayOfChar[i] = c;
/*    */     } 
/* 30 */     return new String(arrayOfChar);
/*    */   }
/*    */   
/*    */   public static void main(String[] paramArrayOfString) {
/* 34 */     if (paramArrayOfString == null || paramArrayOfString.length != 1) {
/* 35 */       System.out.println("Need a username");
/* 36 */       System.exit(1);
/*    */     } 
/* 38 */     String str1 = paramArrayOfString[0];
/* 39 */     String str2 = "!!keykeykey!!";
/* 40 */     System.out.println("Generation password reset link for " + str1);
/* 41 */     System.out.println("Created password reset link: " + (new PasswordResetLink()).createPasswordReset(str1, str2));
/*    */   }
/*    */ }
