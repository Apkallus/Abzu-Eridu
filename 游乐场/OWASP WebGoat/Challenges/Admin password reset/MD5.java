/*     */ import java.io.File;
/*     */ import java.io.FileInputStream;
/*     */ import java.io.IOException;
/*     */ import java.io.InputStream;
/*     */ import java.io.UnsupportedEncodingException;
/*     */ 
/*     */ public class MD5 {
/*     */   private MD5State workingState;
/*     */   
/*     */   private MD5State finalState;
/*     */   
/*     */   private int[] decodeBuffer;
/*     */   
/*     */   public MD5() {
/* 408 */     this.workingState = new MD5State();
/* 417 */     this.finalState = new MD5State();
/* 424 */     this.decodeBuffer = new int[16];
/*     */     reset();
/*     */   }
/*     */   
/*     */   public static void main(String[] paramArrayOfString) {
/*     */     if (paramArrayOfString.length == 0) {
/*     */       System.err.println("Please specify a file.");
/*     */     } else {
/*     */       for (String str : paramArrayOfString) {
/*     */         try {
/*     */           System.out.println(getHashString(new File(str)) + " " + str);
/*     */         } catch (IOException iOException) {
/*     */           System.err.println(iOException.getMessage());
/*     */         } 
/*     */       } 
/*     */     } 
/*     */   }
/*     */   
/*     */   public byte[] getHash() {
/*     */     if (!this.finalState.valid) {
/*     */       this.finalState.copy(this.workingState);
/*     */       long l = this.finalState.bitCount;
/*     */       int i = (int)(l >>> 3L & 0x3FL);
/*     */       int j = (i < 56) ? (56 - i) : (120 - i);
/*     */       update(this.finalState, padding, 0, j);
/*     */       update(this.finalState, encode(l), 0, 8);
/*     */       this.finalState.valid = true;
/*     */     } 
/*     */     return encode(this.finalState.state, 16);
/*     */   }
/*     */   
/*     */   public String getHashString() {
/*     */     return toHex(getHash());
/*     */   }
/*     */   
/*     */   public static byte[] getHash(byte[] paramArrayOfbyte) {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramArrayOfbyte);
/*     */     return mD5.getHash();
/*     */   }
/*     */   
/*     */   public static String getHashString(byte[] paramArrayOfbyte) {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramArrayOfbyte);
/*     */     return mD5.getHashString();
/*     */   }
/*     */   
/*     */   public static byte[] getHash(InputStream paramInputStream) throws IOException {
/*     */     MD5 mD5 = new MD5();
/*     */     byte[] arrayOfByte = new byte[1024];
/*     */     int i;
/*     */     while ((i = paramInputStream.read(arrayOfByte)) != -1)
/*     */       mD5.update(arrayOfByte, i); 
/*     */     return mD5.getHash();
/*     */   }
/*     */   
/*     */   public static String getHashString(InputStream paramInputStream) throws IOException {
/*     */     MD5 mD5 = new MD5();
/*     */     byte[] arrayOfByte = new byte[1024];
/*     */     int i;
/*     */     while ((i = paramInputStream.read(arrayOfByte)) != -1)
/*     */       mD5.update(arrayOfByte, i); 
/*     */     return mD5.getHashString();
/*     */   }
/*     */   
/*     */   public static byte[] getHash(File paramFile) throws IOException {
/*     */     FileInputStream fileInputStream = new FileInputStream(paramFile);
/*     */     byte[] arrayOfByte = getHash(fileInputStream);
/*     */     fileInputStream.close();
/*     */     return arrayOfByte;
/*     */   }
/*     */   
/*     */   public static String getHashString(File paramFile) throws IOException {
/*     */     FileInputStream fileInputStream = new FileInputStream(paramFile);
/*     */     String str = getHashString(fileInputStream);
/*     */     fileInputStream.close();
/*     */     return str;
/*     */   }
/*     */   
/*     */   public static byte[] getHash(String paramString) {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramString);
/*     */     return mD5.getHash();
/*     */   }
/*     */   
/*     */   public static String getHashString(String paramString) {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramString);
/*     */     return mD5.getHashString();
/*     */   }
/*     */   
/*     */   public static byte[] getHash(String paramString1, String paramString2) throws UnsupportedEncodingException {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramString1, paramString2);
/*     */     return mD5.getHash();
/*     */   }
/*     */   
/*     */   public static String getHashString(String paramString1, String paramString2) throws UnsupportedEncodingException {
/*     */     MD5 mD5 = new MD5();
/*     */     mD5.update(paramString1, paramString2);
/*     */     return mD5.getHashString();
/*     */   }
/*     */   
/*     */   public void reset() {
/*     */     this.workingState.reset();
/*     */     this.finalState.valid = false;
/*     */   }
/*     */   
/*     */   public String toString() {
/*     */     return getHashString();
/*     */   }
/*     */   
/*     */   private void update(MD5State paramMD5State, byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
/*     */     this.finalState.valid = false;
/*     */     if (paramInt2 + paramInt1 > paramArrayOfbyte.length)
/*     */       paramInt2 = paramArrayOfbyte.length - paramInt1; 
/*     */     int i = (int)(paramMD5State.bitCount >>> 3L) & 0x3F;
/*     */     MD5State mD5State = paramMD5State;
/*     */     mD5State.bitCount = mD5State.bitCount + (paramInt2 << 3);
/*     */     int j = 64 - i;
/*     */     int k = 0;
/*     */     if (paramInt2 >= j) {
/*     */       System.arraycopy(paramArrayOfbyte, paramInt1, paramMD5State.buffer, i, j);
/*     */       transform(paramMD5State, decode(paramMD5State.buffer, 64, 0));
/*     */       for (k = j; k + 63 < paramInt2; k += 64)
/*     */         transform(paramMD5State, decode(paramArrayOfbyte, 64, k)); 
/*     */       i = 0;
/*     */     } 
/*     */     if (k < paramInt2)
/*     */       for (int m = k; k < paramInt2; k++)
/*     */         paramMD5State.buffer[i + k - m] = paramArrayOfbyte[k + paramInt1];  
/*     */   }
/*     */   
/*     */   public void update(byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
/*     */     update(this.workingState, paramArrayOfbyte, paramInt1, paramInt2);
/*     */   }
/*     */   
/*     */   public void update(byte[] paramArrayOfbyte, int paramInt) {
/*     */     update(paramArrayOfbyte, 0, paramInt);
/*     */   }
/*     */   
/*     */   public void update(byte[] paramArrayOfbyte) {
/*     */     update(paramArrayOfbyte, 0, paramArrayOfbyte.length);
/*     */   }
/*     */   
/*     */   public void update(byte paramByte) {
/*     */     byte[] arrayOfByte = new byte[1];
/*     */     arrayOfByte[0] = paramByte;
/*     */     update(arrayOfByte, 1);
/*     */   }
/*     */   
/*     */   public void update(String paramString) {
/*     */     update(paramString.getBytes());
/*     */   }
/*     */   
/*     */   public void update(String paramString1, String paramString2) throws UnsupportedEncodingException {
/*     */     update(paramString1.getBytes(paramString2));
/*     */   }
/*     */   
/* 432 */   private static final byte[] padding = new byte[] { 
/* 432 */       Byte.MIN_VALUE, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
/* 432 */       0, 0, 0, 0 };
/*     */   
/*     */   private class MD5State {
/*     */     private boolean valid = true;
/*     */     
/*     */     private void reset() {
/* 464 */       this.state[0] = 1732584193;
/* 465 */       this.state[1] = -271733879;
/* 466 */       this.state[2] = -1732584194;
/* 467 */       this.state[3] = 271733878;
/* 469 */       this.bitCount = 0L;
/*     */     }
/*     */     
/* 477 */     private int[] state = new int[4];
/*     */     
/*     */     private long bitCount;
/*     */     
/* 491 */     private byte[] buffer = new byte[64];
/*     */     
/*     */     private MD5State() {
/* 494 */       reset();
/*     */     }
/*     */     
/*     */     private void copy(MD5State param1MD5State) {
/* 504 */       System.arraycopy(param1MD5State.buffer, 0, this.buffer, 0, this.buffer.length);
/* 505 */       System.arraycopy(param1MD5State.state, 0, this.state, 0, this.state.length);
/* 506 */       this.valid = param1MD5State.valid;
/* 507 */       this.bitCount = param1MD5State.bitCount;
/*     */     }
/*     */   }
/*     */   
/*     */   private static String toHex(byte[] paramArrayOfbyte) {
/* 521 */     StringBuffer stringBuffer = new StringBuffer(paramArrayOfbyte.length * 2);
/* 522 */     for (byte b : paramArrayOfbyte) {
/* 523 */       int i = b & 0xFF;
/* 524 */       if (i < 16)
/* 527 */         stringBuffer.append("0"); 
/* 529 */       stringBuffer.append(Integer.toHexString(i));
/*     */     } 
/* 531 */     return stringBuffer.toString();
/*     */   }
/*     */   
/*     */   private static int FF(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
/* 535 */     paramInt1 += paramInt2 & paramInt3 | (paramInt2 ^ 0xFFFFFFFF) & paramInt4;
/* 536 */     paramInt1 += paramInt5;
/* 537 */     paramInt1 += paramInt7;
/* 539 */     paramInt1 = paramInt1 << paramInt6 | paramInt1 >>> 32 - paramInt6;
/* 540 */     return paramInt1 + paramInt2;
/*     */   }
/*     */   
/*     */   private static int GG(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
/* 544 */     paramInt1 += paramInt2 & paramInt4 | paramInt3 & (paramInt4 ^ 0xFFFFFFFF);
/* 545 */     paramInt1 += paramInt5;
/* 546 */     paramInt1 += paramInt7;
/* 548 */     paramInt1 = paramInt1 << paramInt6 | paramInt1 >>> 32 - paramInt6;
/* 549 */     return paramInt1 + paramInt2;
/*     */   }
/*     */   
/*     */   private static int HH(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
/* 553 */     paramInt1 += paramInt2 ^ paramInt3 ^ paramInt4;
/* 554 */     paramInt1 += paramInt5;
/* 555 */     paramInt1 += paramInt7;
/* 557 */     paramInt1 = paramInt1 << paramInt6 | paramInt1 >>> 32 - paramInt6;
/* 558 */     return paramInt1 + paramInt2;
/*     */   }
/*     */   
/*     */   private static int II(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
/* 562 */     paramInt1 += paramInt3 ^ (paramInt2 | paramInt4 ^ 0xFFFFFFFF);
/* 563 */     paramInt1 += paramInt5;
/* 564 */     paramInt1 += paramInt7;
/* 566 */     paramInt1 = paramInt1 << paramInt6 | paramInt1 >>> 32 - paramInt6;
/* 567 */     return paramInt1 + paramInt2;
/*     */   }
/*     */   
/*     */   private static byte[] encode(long paramLong) {
/* 571 */     byte[] arrayOfByte = new byte[8];
/* 572 */     arrayOfByte[0] = (byte)(int)(paramLong & 0xFFL);
/* 573 */     arrayOfByte[1] = (byte)(int)(paramLong >>> 8L & 0xFFL);
/* 574 */     arrayOfByte[2] = (byte)(int)(paramLong >>> 16L & 0xFFL);
/* 575 */     arrayOfByte[3] = (byte)(int)(paramLong >>> 24L & 0xFFL);
/* 576 */     arrayOfByte[4] = (byte)(int)(paramLong >>> 32L & 0xFFL);
/* 577 */     arrayOfByte[5] = (byte)(int)(paramLong >>> 40L & 0xFFL);
/* 578 */     arrayOfByte[6] = (byte)(int)(paramLong >>> 48L & 0xFFL);
/* 579 */     arrayOfByte[7] = (byte)(int)(paramLong >>> 56L & 0xFFL);
/* 580 */     return arrayOfByte;
/*     */   }
/*     */   
/*     */   private static byte[] encode(int[] paramArrayOfint, int paramInt) {
/* 584 */     byte[] arrayOfByte = new byte[paramInt];
/* 586 */     for (byte b2 = 0, b1 = b2; b2 < paramInt; b1++, b2 += 4) {
/* 587 */       arrayOfByte[b2] = (byte)(paramArrayOfint[b1] & 0xFF);
/* 588 */       arrayOfByte[b2 + 1] = (byte)(paramArrayOfint[b1] >>> 8 & 0xFF);
/* 589 */       arrayOfByte[b2 + 2] = (byte)(paramArrayOfint[b1] >>> 16 & 0xFF);
/* 590 */       arrayOfByte[b2 + 3] = (byte)(paramArrayOfint[b1] >>> 24 & 0xFF);
/*     */     } 
/* 592 */     return arrayOfByte;
/*     */   }
/*     */   
/*     */   private int[] decode(byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
/* 597 */     for (byte b2 = 0, b1 = b2; b2 < paramInt1; b1++, b2 += 4)
/* 598 */       this.decodeBuffer[b1] = paramArrayOfbyte[b2 + paramInt2] & 0xFF | (paramArrayOfbyte[b2 + 1 + paramInt2] & 0xFF) << 8 | (paramArrayOfbyte[b2 + 2 + paramInt2] & 0xFF) << 16 | (paramArrayOfbyte[b2 + 3 + paramInt2] & 0xFF) << 24; 
/* 605 */     return this.decodeBuffer;
/*     */   }
/*     */   
/*     */   private static void transform(MD5State paramMD5State, int[] paramArrayOfint) {
/* 609 */     int i = paramMD5State.state[0];
/* 610 */     int j = paramMD5State.state[1];
/* 611 */     int k = paramMD5State.state[2];
/* 612 */     int m = paramMD5State.state[3];
/* 615 */     i = FF(i, j, k, m, paramArrayOfint[0], 7, -680876936);
/* 616 */     m = FF(m, i, j, k, paramArrayOfint[1], 12, -389564586);
/* 617 */     k = FF(k, m, i, j, paramArrayOfint[2], 17, 606105819);
/* 618 */     j = FF(j, k, m, i, paramArrayOfint[3], 22, -1044525330);
/* 619 */     i = FF(i, j, k, m, paramArrayOfint[4], 7, -176418897);
/* 620 */     m = FF(m, i, j, k, paramArrayOfint[5], 12, 1200080426);
/* 621 */     k = FF(k, m, i, j, paramArrayOfint[6], 17, -1473231341);
/* 622 */     j = FF(j, k, m, i, paramArrayOfint[7], 22, -45705983);
/* 623 */     i = FF(i, j, k, m, paramArrayOfint[8], 7, 1770035416);
/* 624 */     m = FF(m, i, j, k, paramArrayOfint[9], 12, -1958414417);
/* 625 */     k = FF(k, m, i, j, paramArrayOfint[10], 17, -42063);
/* 626 */     j = FF(j, k, m, i, paramArrayOfint[11], 22, -1990404162);
/* 627 */     i = FF(i, j, k, m, paramArrayOfint[12], 7, 1804603682);
/* 628 */     m = FF(m, i, j, k, paramArrayOfint[13], 12, -40341101);
/* 629 */     k = FF(k, m, i, j, paramArrayOfint[14], 17, -1502002290);
/* 630 */     j = FF(j, k, m, i, paramArrayOfint[15], 22, 1236535329);
/* 633 */     i = GG(i, j, k, m, paramArrayOfint[1], 5, -165796510);
/* 634 */     m = GG(m, i, j, k, paramArrayOfint[6], 9, -1069501632);
/* 635 */     k = GG(k, m, i, j, paramArrayOfint[11], 14, 643717713);
/* 636 */     j = GG(j, k, m, i, paramArrayOfint[0], 20, -373897302);
/* 637 */     i = GG(i, j, k, m, paramArrayOfint[5], 5, -701558691);
/* 638 */     m = GG(m, i, j, k, paramArrayOfint[10], 9, 38016083);
/* 639 */     k = GG(k, m, i, j, paramArrayOfint[15], 14, -660478335);
/* 640 */     j = GG(j, k, m, i, paramArrayOfint[4], 20, -405537848);
/* 641 */     i = GG(i, j, k, m, paramArrayOfint[9], 5, 568446438);
/* 642 */     m = GG(m, i, j, k, paramArrayOfint[14], 9, -1019803690);
/* 643 */     k = GG(k, m, i, j, paramArrayOfint[3], 14, -187363961);
/* 644 */     j = GG(j, k, m, i, paramArrayOfint[8], 20, 1163531501);
/* 645 */     i = GG(i, j, k, m, paramArrayOfint[13], 5, -1444681467);
/* 646 */     m = GG(m, i, j, k, paramArrayOfint[2], 9, -51403784);
/* 647 */     k = GG(k, m, i, j, paramArrayOfint[7], 14, 1735328473);
/* 648 */     j = GG(j, k, m, i, paramArrayOfint[12], 20, -1926607734);
/* 651 */     i = HH(i, j, k, m, paramArrayOfint[5], 4, -378558);
/* 652 */     m = HH(m, i, j, k, paramArrayOfint[8], 11, -2022574463);
/* 653 */     k = HH(k, m, i, j, paramArrayOfint[11], 16, 1839030562);
/* 654 */     j = HH(j, k, m, i, paramArrayOfint[14], 23, -35309556);
/* 655 */     i = HH(i, j, k, m, paramArrayOfint[1], 4, -1530992060);
/* 656 */     m = HH(m, i, j, k, paramArrayOfint[4], 11, 1272893353);
/* 657 */     k = HH(k, m, i, j, paramArrayOfint[7], 16, -155497632);
/* 658 */     j = HH(j, k, m, i, paramArrayOfint[10], 23, -1094730640);
/* 659 */     i = HH(i, j, k, m, paramArrayOfint[13], 4, 681279174);
/* 660 */     m = HH(m, i, j, k, paramArrayOfint[0], 11, -358537222);
/* 661 */     k = HH(k, m, i, j, paramArrayOfint[3], 16, -722521979);
/* 662 */     j = HH(j, k, m, i, paramArrayOfint[6], 23, 76029189);
/* 663 */     i = HH(i, j, k, m, paramArrayOfint[9], 4, -640364487);
/* 664 */     m = HH(m, i, j, k, paramArrayOfint[12], 11, -421815835);
/* 665 */     k = HH(k, m, i, j, paramArrayOfint[15], 16, 530742520);
/* 666 */     j = HH(j, k, m, i, paramArrayOfint[2], 23, -995338651);
/* 669 */     i = II(i, j, k, m, paramArrayOfint[0], 6, -198630844);
/* 670 */     m = II(m, i, j, k, paramArrayOfint[7], 10, 1126891415);
/* 671 */     k = II(k, m, i, j, paramArrayOfint[14], 15, -1416354905);
/* 672 */     j = II(j, k, m, i, paramArrayOfint[5], 21, -57434055);
/* 673 */     i = II(i, j, k, m, paramArrayOfint[12], 6, 1700485571);
/* 674 */     m = II(m, i, j, k, paramArrayOfint[3], 10, -1894986606);
/* 675 */     k = II(k, m, i, j, paramArrayOfint[10], 15, -1051523);
/* 676 */     j = II(j, k, m, i, paramArrayOfint[1], 21, -2054922799);
/* 677 */     i = II(i, j, k, m, paramArrayOfint[8], 6, 1873313359);
/* 678 */     m = II(m, i, j, k, paramArrayOfint[15], 10, -30611744);
/* 679 */     k = II(k, m, i, j, paramArrayOfint[6], 15, -1560198380);
/* 680 */     j = II(j, k, m, i, paramArrayOfint[13], 21, 1309151649);
/* 681 */     i = II(i, j, k, m, paramArrayOfint[4], 6, -145523070);
/* 682 */     m = II(m, i, j, k, paramArrayOfint[11], 10, -1120210379);
/* 683 */     k = II(k, m, i, j, paramArrayOfint[2], 15, 718787259);
/* 684 */     j = II(j, k, m, i, paramArrayOfint[9], 21, -343485551);
/* 686 */     paramMD5State.state[0] = paramMD5State.state[0] + i;
/* 687 */     paramMD5State.state[1] = paramMD5State.state[1] + j;
/* 688 */     paramMD5State.state[2] = paramMD5State.state[2] + k;
/* 689 */     paramMD5State.state[3] = paramMD5State.state[3] + m;
/*     */   }
/*     */ }
